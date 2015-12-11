from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.select import Select
from selenium.common.exceptions import NoSuchElementException


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


def select_text(self, coordinate, text):
    if not isinstance(coordinate, Select):
        if isinstance(coordinate, str):
            element = self.get_element(coordinate)
        else:
            element = coordinate
        selection = Select(element)
    else:
        selection = coordinate
    try:
        selection.select_by_visible_text(text)
        return True
    except NoSuchElementException:
        available_selections = []
        for option in selection.options:
            if text in option.text:
                selection.select_by_visible_text(option.text)
                return True
            available_selections.append(option.text)
        print("[Error!] Selection not found: {}".format(text))
        print("Available Selections\n {}".format(available_selections))


def submit_btn(self, value, success=None):
    """This presses an input button with type=submit.
    Success must be given as a tuple of a (coordinate, timeout).
    Use (coordinate,) if you want to use the default timeout."""
    self.press("css=input[value='{}']".format(value))
    if success is not None:
        assert self.is_available(*success)
