import subprocess
import shlex
from datetime import datetime

from polarbird.settings import settings

DATETIME_ORIGINAL_FORMAT = '%a %b %d %H:%M:%S %z %Y'

def convert_datetime(tweet_datetime):
    """
    Converts Twitter datetime format to user defined format, if set, otherwise
    to default format.
    """
    dt = datetime.strptime(tweet_datetime, DATETIME_ORIGINAL_FORMAT)
    dt = dt.astimezone()
    converted_datetime = dt.strftime(settings.DATETIME_FORMAT)

    return converted_datetime

def show_notification(tweet):
    """
    Show notification dialog on Linux
    """
    notification_command = settings.NOTIFICATION_COMMAND
    if not notification_command:
        return

    if 'retweeted_status' in tweet:
        username = '@{}'.format(tweet['retweeted_status']['user']['screen_name'])
        text = tweet['retweeted_status']['text']
    else:
        username = '@{}'.format(tweet['user']['screen_name'])
        text = tweet['text']

    text = text.replace('\'', '\\\'')
    text = text.replace('"', '\\"')
    notification_command = notification_command.format(username=username, text=text)
    arguments = shlex.split(notification_command)
    subprocess.Popen(arguments)

def compute_used_lines(window, text):
    """
    Compute how many lines is needed for text to be
    printed on screen.
    """
    window_size = window.getmaxyx()
    used_lines = int(len(text) / (window_size[1]) + 1)

    return used_lines
