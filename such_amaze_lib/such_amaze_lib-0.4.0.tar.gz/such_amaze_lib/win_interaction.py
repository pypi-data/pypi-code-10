import win32api
import time

import win32con


class Mouse:
    """
        Wrapper for better user experience
    """

    def __init__(self):
        pass

    @staticmethod
    def set_position(coordinate, padding=(0, 0)):
        """
            Move mouse to position 'coordinate' with padding or not

        :param coordinate: new coordinate of the mouse
        :param padding: positional padding
        """
        x, y = coordinate[0] + padding[0], coordinate[1] + padding[1]
        win32api.SetCursorPos((x, y))

    @staticmethod
    def get_position(padding=(0, 0)):
        """
            Return cursor position
        :param padding: positional padding
        :return: tuple
        """
        x, y = win32api.GetCursorPos()
        return x - padding[0], y - padding[0]

    @staticmethod
    def click(is_right_click, holding_time=.1):
        """
            Create click down then up event 'during holding_time' seconds

        :param is_right_click: is a right or a left click
        """
        down = win32con.MOUSEEVENTF_RIGHTDOWN
        up = win32con.MOUSEEVENTF_RIGHTUP
        if not is_right_click:
            down = win32con.MOUSEEVENTF_LEFTDOWN
            up = win32con.MOUSEEVENTF_LEFTUP
        win32api.mouse_event(down, 0, 0)
        time.sleep(holding_time)
        win32api.mouse_event(up, 0, 0)

    def click_at(self, coordinate, padding, is_right_click=False):
        """
            Move cursor at coordinate then click

        :param coordinate: the position to move to
        :param padding: positional padding
        :param is_right_click: is click right or left
        """
        self.set_position(coordinate, padding)
        self.click(is_right_click)
