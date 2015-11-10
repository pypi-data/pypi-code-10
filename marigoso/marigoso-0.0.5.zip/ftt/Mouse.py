from selenium.webdriver.remote.webelement import WebElement


def press(self, coordinate, success=None):
    """Success must be given as a tuple of a (coordinate, timeout).
    Use (coordinate,) if you want to use the default timeout."""
    if type(coordinate) is WebElement:
        coordinate.click()
    else:
        self.get_element(coordinate).click()
    if success is not None:
        assert self.is_available(*success)


def press_available(self, coordinate, timeout=2):
    if self.is_available(coordinate, timeout):
        self.press(coordinate)


def submit_btn(self, value, success=None):
    """This presses an input button with type=submit.
    Success must be given as a tuple of a (coordinate, timeout).
    Use (coordinate,) if you want to use the default timeout."""
    self.press("css=input[value='{}']".format(value))
    if success is not None:
        assert self.is_available(*success)
