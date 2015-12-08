"""
    Windows mouse interaction
"""

import win32api
import time

import win32con


def set_position(coordinate, padding=(0, 0)):
    """
        Move mouse to position 'coordinate' with padding or not

        :Example:

            >>> current_pos = get_position()
            >>> new_pos = current_pos[0] + 100, current_pos[1] + 100
            >>> set_position(current_pos)

        Is strictly the same as

            >>> set_position(get_position(), (100, 100))

    :param coordinate: new coordinate of the mouse
    :param padding: positional padding
    """
    x, y = coordinate[0] + padding[0], coordinate[1] + padding[1]
    win32api.SetCursorPos((x, y))


def get_position(padding=(0, 0)):
    """
        Return cursor position

        :Example:

        >>> last_position = get_position()
        >>> set_position((0, 0))
        >>> print get_position()
        (0, 0)
        >>> set_position(last_position)

    :param padding: positional padding
    :return: tuple
    """
    x, y = win32api.GetCursorPos()
    return x - padding[0], y - padding[1]


def click(is_right_click=False, holding_time=.1):
    """
        Create click down then up event 'during holding_time' seconds

    :param is_right_click: is a right or a left click
    :param holding_time: time before releasing the mouse button
    """
    down = win32con.MOUSEEVENTF_RIGHTDOWN
    up = win32con.MOUSEEVENTF_RIGHTUP
    if not is_right_click:
        down = win32con.MOUSEEVENTF_LEFTDOWN
        up = win32con.MOUSEEVENTF_LEFTUP
    win32api.mouse_event(down, 0, 0)
    time.sleep(holding_time)
    win32api.mouse_event(up, 0, 0)


def click_at(coordinate, padding=(0, 0), is_right_click=False, holding_time=.1):
    """
        Move cursor at coordinate then click

    :param coordinate: the position to move to
    :param padding: positional padding
    :param is_right_click: is click right or left
    """
    set_position(coordinate, padding)
    click(is_right_click, holding_time)
