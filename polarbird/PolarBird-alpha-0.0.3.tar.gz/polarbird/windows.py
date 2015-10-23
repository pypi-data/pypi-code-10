from collections import OrderedDict
from datetime import datetime
import twitter
import curses

from polarbird.settings import settings
from polarbird.utils import convert_datetime, compute_used_lines
from polarbird.colors import colors
from polarbird.commands import HomeCommand, RetweetCommand, WindowCommand

class Window(object):
    """
    Base class for all ncurses windows.
    """

    def __init__(self, screen, lines, cols, y=0, x=0):
        self.title = 'Unnamed window'
        self._window = curses.newwin(lines, cols, y, x)
        self._screen = screen

    def resize(self, lines, cols):
        """
        Resize ncurses window.
        """
        self._window.resize(lines, cols)

    def refresh(self):
        """
        Clear and refresh window. Subclasses should override this
        to provide custom data in window.
        """
        self._window.clear()
        self._window.refresh()

    def move(self, y, x):
        """
        Move ncurses window to new location.
        """
        self._window.mvwin(y, x)

class Screen(object):
    """
    Main ncurses window (screen) used as container for all other windows.
    """

    RESERVED_BOTTOM_LINES = 2

    INFO_WINDOW = 0
    TWEET_WINDOW = 1

    def __init__(self, screen, app):
        self._screen = screen
        self._app = app
        curses.start_color()
        self._windows = [
            InfoWindow(
                self, curses.LINES - Screen.RESERVED_BOTTOM_LINES, curses.COLS
            ),
            TweetWindow(
                self, curses.LINES - Screen.RESERVED_BOTTOM_LINES, curses.COLS,
                self._app.tweet_database
            ),
        ]
        self._current_window_id = 0
        self._status_window = StatusWindow(self)
        self.command_line_window = CommandLineWindow(self, app)

    def get_window(self, window_id):
        """
        Return window by its id.
        """
        return self._windows[window_id]

    def switch_to_left_window(self):
        """
        Cycle windows to the left.
        """
        if self._current_window_id == 0:
            self._current_window_id = len(self._windows) - 1
        else:
            self._current_window_id -= 1

    def switch_to_right_window(self):
        """
        Cycle windows to the right.
        """
        if self._current_window_id == len(self._windows) - 1:
            self._current_window_id = 0
        else:
            self._current_window_id += 1

    def get_windows(self):
        """
        Return all main windows on screen.
        """
        return self._windows

    def is_current_window(self, window):
        """
        Check if window is currently displayed.
        """
        return self._windows[self._current_window_id] == window

    def refresh_current_window(self):
        """
        Refresh current displayed window.
        """
        self._windows[self._current_window_id].refresh()

    def handle_resize(self):
        """
        Handle resize event. Resize and move window to/on right values.
        """
        y, x = self._screen.getmaxyx()
        for window in self._windows:
            window.resize(y - Screen.RESERVED_BOTTOM_LINES, x)
        self.command_line_window.resize(1, x)
        self.command_line_window.move(y - 1, 0)
        self._status_window.resize(1, x)
        self._status_window.move(y - 2, 0)
        self._windows[self._current_window_id].refresh()
        self.command_line_window.refresh()
        self._status_window.refresh()

    def refresh_all_windows(self):
        """
        Refresh current, command line and status window.
        """
        self.refresh_current_window()
        self.command_line_window.refresh()
        self._status_window.refresh()

class TweetWindow(Window):
    """
    Window where tweets are displayed
    """

    def __init__(self, screen, lines, cols, tweet_database):
        super(TweetWindow, self).__init__(screen, lines, cols)
        self.title = 'Tweets'
        self._tweet_database = tweet_database

    def refresh(self):
        """
        Refresh window so it display latest tweets.
        """
        self._window.clear()
        last_tweets = self._get_tweets()
        start_line = 0
        for tweet in last_tweets:
            used_lines = self._print_tweet(tweet, start_line)
            start_line += used_lines
        self._window.refresh()

    def _print_tweet(self, tweet, line_number):
        """
        Print formatted tweet
        """
        formatted = self._format_tweet(tweet)
        used_lines = compute_used_lines(self._window, formatted)

        self._window.addstr(line_number, 0, formatted)

        return int(used_lines)

    def _format_tweet(self, tweet):
        """
        Format tweet by user format, if set, otherwise use default format
        """
        created_at = convert_datetime(tweet[1]['created_at'])
        if 'retweeted_status' in tweet[1]:
            screen_name = tweet[1]['user']['screen_name']
            text = tweet[1]['retweeted_status']['text']
            used_format = settings.RETWEET_FORMAT
        else:
            screen_name = tweet[1]['user']['screen_name']
            text = tweet[1]['text']
            used_format = settings.TWEET_FORMAT
        text = text.replace('\n', '')
        formatted = used_format.format(
            created_at=created_at, screen_name=screen_name, text=text, key=tweet[0],
            colors=colors
        )

        return formatted

    def _get_tweets(self):
        """
        Fetch tweets which will be printed. It fetch only tweets that can be fully
        displayed.
        """
        keys = reversed(self._tweet_database.keys())
        total_lines = 0
        tweets = OrderedDict()
        for key in keys:
            tweet = self._tweet_database[key]
            formatted = self._format_tweet((key, tweet))
            used_lines = compute_used_lines(self._window, formatted)
            window_size = self._window.getmaxyx()
            if total_lines + used_lines <= window_size[0]:
                total_lines += used_lines
                tweets[key] = tweet

        return reversed(list(tweets.items()))

class CommandLineWindow(Window):
    """
    Command line handler for commands from user
    """

    CMD_PREFIX = '>> '

    def __init__(self, screen, app):
        super(CommandLineWindow, self).__init__(
            screen, 1, curses.COLS, curses.LINES - 1, 0
        )
        curses.init_pair(1, 0, 12)
        self._window.bkgd(' ', curses.color_pair(1))
        self._app = app
        self._commands = {}
        self._register_commands()
        self._user_input = ''

    def get_character(self):
        """
        Return input character. This include special curses characters/keys
        such as KEY_RESIZE etc.
        """
        self._window.addstr(0, 0, CommandLineWindow.CMD_PREFIX)
        max_chars = self._window.getmaxyx()[1] - 4
        character = self._window.get_wch(
            0, len(CommandLineWindow.CMD_PREFIX) + len(self._user_input[-max_chars:])
        )

        return character

    def handle_input(self, character):
        """
        Handle character input mostly without special keys.
        """
        if character == '\n':
            if self._user_input and self._user_input[0] == '/':
                self._handle_command(self._user_input)
            elif self._user_input:
                self._send_tweet(self._user_input)
            self._user_input = ''
        elif character == curses.KEY_BACKSPACE or ord(character) == 127:
            self._user_input = self._user_input[:-1]
        elif character == curses.KEY_DL or ord(character) == 21:
            self._user_input = ''
        else:
            self._user_input += character

    def refresh(self):
        """
        Clear and redraw window.
        """
        max_chars = self._window.getmaxyx()[1] - 4
        self._window.clear()
        self._window.addstr(0, 0, CommandLineWindow.CMD_PREFIX)
        self._window.addstr(0, 3, self._user_input[-max_chars:])
        self._window.refresh()

    def _get_twitter(self):
        """
        Getting Twitter instance to access API.
        """
        tw = twitter.Twitter(auth=self._app.auth)

        return tw

    def _register_commands(self):
        """
        Register command classes for use in command line.
        """
        commands_cls = (HomeCommand, RetweetCommand, WindowCommand,)
        for cls in commands_cls:
            cmd = cls(self._app, self._screen.get_window(self._screen.INFO_WINDOW))
            self._commands[cmd.NAME] = cmd

    def _handle_command(self, command):
        """
        Handle command which starts with '/'.
        """
        cmd_and_args = command[1:].split(' ')
        if cmd_and_args[0] == 'exit':
            curses.endwin()
            exit(0)
        elif cmd_and_args[0] == 'help':
            try:
                self._show_help(cmd_and_args[1])
            except IndexError:
                self._show_full_help()
        elif cmd_and_args[0] in self._commands:
            tw = self._get_twitter()
            try:
                self._commands[cmd_and_args[0]].execute(tw, cmd_and_args[1])
            except twitter.TwitterHTTPError as e:
                info_window = self._screen.get_window(self._screen.INFO_WINDOW)
                info_window.add_message(str(e), info_window.ERROR)
            except IndexError:
                self._commands[cmd_and_args[0]].execute(tw)

    def _send_tweet(self, text):
        """
        Send new tweet if message is lesser or equal to 140 characters.
        """
        t = self._get_twitter()
        try:
            t.statuses.update(status=text)
        except twitter.TwitterHTTPError as e:
            info_window = self._screen.get_window(self._screen.INFO_WINDOW)
            info_window.add_message(str(e), info_window.ERROR)

    def _show_help(self, cmd):
        """
        Show help for specified command.
        """
        info_window = self._screen.get_window(self._screen.INFO_WINDOW)
        if cmd in self._commands:
            info_window.add_message(self._commands[cmd].HELP_TEXT)

    def _show_full_help(self):
        """
        Show complete help page with all available commands.
        """
        builtin_commands = ['help', 'exit']
        info_window = self._screen.get_window(self._screen.INFO_WINDOW)
        info_window.add_message(
            'List of available commands: {commands}'.format(
                commands=', '.join(list(self._commands.keys()) + builtin_commands)
            )
        )

class StatusWindow(Window):
    """
    Shows information about opened windows with current window higlighted.
    """

    def __init__(self, screen):
        super(StatusWindow, self).__init__(
            screen, 1, curses.COLS, curses.LINES - 2, 0
        )
        curses.init_pair(1, 0, 12)
        curses.init_pair(2, 7, 1)
        curses.init_pair(3, 2, 0)  # INFO level color
        curses.init_pair(4, 3, 0)  # WARNING level color
        curses.init_pair(5, 1, 0)  # ERORR level color
        self._window.bkgd(' ', curses.color_pair(1))

    def refresh(self):
        position = 0
        for i, window in enumerate(self._screen.get_windows()):
            window_text = '{}: {}'.format(i, window.title)
            if self._screen.is_current_window(window):
                self._window.addstr(0, position, window_text, curses.color_pair(2))
            else:
                self._window.addstr(0, position, window_text)
            position += len(window_text) + 2
        self._window.refresh()

class InfoWindow(Window):
    """
    Info window where log messages (e.g. errors) are displayed.
    """

    INFO = 0
    WARNING = 1
    ERROR = 2

    def __init__(self, screen, lines, cols):
        super(InfoWindow, self).__init__(screen, lines, cols)
        self.title = 'Info'
        self._messages = []

    def refresh(self):
        self._window.clear()
        start_line = 0
        for message in self._messages:
            if message[1] == InfoWindow.INFO:
                color_attr = curses.color_pair(3)
            elif message[1] == InfoWindow.WARNING:
                color_attr = curses.color_pair(4)
            elif message[1] == InfoWindow.ERROR:
                color_attr = curses.color_pair(5)
            text = '[{}] {}'.format(message[0], message[2])
            self._window.addstr(
                start_line, 0, text, color_attr
            )
            start_line += compute_used_lines(self._window, text)
        self._window.refresh()

    def add_message(self, message, level=None):
        """
        Add message to info window with urgency level (info, warning, error).
        """
        if not level:
            level = InfoWindow.INFO
        date = datetime.now().strftime(settings.DATETIME_FORMAT)
        self._messages.append((date, level, message))
