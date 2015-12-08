# coding=utf-8
"""
    Windows screen interaction
"""
import win32api
import win32gui
import time
from PIL import ImageGrab

# Screen resolution
resolution = win32api.GetSystemMetrics(0), win32api.GetSystemMetrics(1)


class Win:
    """
        Wrapper for win32 api windows
        type(self.name) = <type 'unicode'>
    """

    def __init__(self, hwnd):
        rect = win32gui.GetWindowRect(hwnd)
        x, y = rect[0], rect[1]
        width, height = rect[2] - x, rect[3] - y
        self.hwnd = hwnd
        self.name = win32gui.GetWindowText(hwnd).decode('mbcs')
        self.position = x, y
        self.size = width, height

    @property
    def middle(self):
        """Return the middle position of the window"""
        return self.position[0] + self.size[0] / 2, self.position[1] + self.size[1] / 2

    def __repr__(self):
        return '[{}] {}:\t{}\t{}x{}'.format(self.hwnd, self.name.encode('mbcs'), self.position, self.size[0],
                                            self.size[1])


def list_windows():
    """
        Return a list of Win of all existing windows

    :return: list of Win
    """
    win_list = list()

    def callback(hwnd, extra):
        win = Win(hwnd)
        win_list.append(win)

    win32gui.EnumWindows(callback, None)
    return win_list


def find_window(window_name):
    """
        Find a windows according to its exact name.
        Return None if nothing match.

    :param window_name: windows exact name
    :return: Win
    """
    hwnd = win32gui.FindWindow(None, window_name)
    return Win(hwnd)


def find_windows(hint):
    """
        Find windows by it's name. Look if hint is contain inside the window label.
        Return an empty list if nothing is found.

    :param hint: window label hint
    :return: list of Win
    """
    l = list()
    for win in list_windows():
        if hint.lower() in win.name.lower():
            l.append(win)
    return l


def move_window(win, position, size, use_centre=False):
    """
        Move a window to position and rescale it if size is given.
        Return a new updated windows

        :Example:
            >>> windows = find_windows(u'google')
            >>> for w in windows:
            ...     mid_res = resolution[0] / 2, resolution[1] / 2
            ...     move_window(w, mid_res, mid_res, use_centre=True)
            ...

    :param win: Win
    :param position: windows position to move
    :param size: the new window size
    :return Win
    """
    if use_centre:
        position = position[0] - size[0] / 2, position[1] - size[1] / 2
    win32gui.MoveWindow(win.hwnd, position[0], position[1], size[0], size[1], True)
    return Win(win.hwnd)


def capture(position=None, size=None, is_saved=True, path='screen_shot_{}.png'.format(int(time.time()))):
    """
        Return a PIL Image of the corresponding position and size? If position or size is None,
        a full screen capture will be done.

    :param position: upper left position
    :param size: image size (width, height)
    :param is_saved: is image will be save
    :param path: if is_saved, is the path location
    :return: Image
    """
    box = None
    if position is not None and size is not None:
        box = (position[0], position[1], position[0] + size[0], position[1] + size[1])
    im = ImageGrab.grab(box)
    if is_saved:
        im.save(path, 'PNG')
    return im
