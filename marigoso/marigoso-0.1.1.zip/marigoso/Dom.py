
import types
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from .FTTException import FTTException

TIMEOUT = 5
ONE, ALL = 0, 1


def get_all(self, coordinate, timeout=TIMEOUT):
    return self.get_element(coordinate, all=True, timeout=timeout)


def get_children(self, coordinate, timeout=TIMEOUT):
    return self.get_child(coordinate, all=True, timeout=timeout)


def get_element(self, coordinate, child=None, all=None, timeout=TIMEOUT):
    find = {
        'css=':   ("find_element_by_css_selector", "find_elements_by_css_selector"),
        'xpath=': ("find_element_by_xpath", "find_elements_by_xpath"),
        'link=':  ("find_element_by_link_text", "find_elements_by_link_text"),
        'class=': ("find_element_by_class_name", "find_elements_by_class_name"),
        'id=':    ("find_element_by_id", "find_elements_by_id"),
        'name=':  ("find_element_by_name", "find_elements_by_name"),
        'plink=': ("find_element_by_partial_link_text", "find_elements_by_partial_link_text"),
        'tag=':   ("find_element_by_tag_name", "find_elements_by_tag_name")
    }
    if isinstance(coordinate, str):
        if "=" not in coordinate:
            if all is None:
                return self.wait_for(getattr(self, find['link='][ONE]), coordinate, timeout)
            return self.wait_for(getattr(self, find['link='][ALL]), coordinate)
        reference, locator = self, coordinate
    else:
        reference, locator = coordinate, child

    # Try the most commonly used selectors
    for by in ['css=', 'xpath=', 'id=', 'name=', 'tag=', 'class=', 'plink', 'link']:
        if locator.startswith(by):
            locator = locator.replace(by, '')
            if all is None:
                # Get the element returned by wait_for
                element = self.wait_for(getattr(reference, find[by][ONE]), locator, timeout)
                # Give the element the ability to grab displayed element
                element.wait_for = types.MethodType(wait_for, element)
                # Give the element the ability to get a child or all children
                element.get_child = types.MethodType(get_element, element)
                element.get_children = types.MethodType(get_children, element)
                # Return the groomed element
                return element
            else:
                # Get the elements returned by wait_for
                elements = self.wait_for(getattr(reference, find[by][ALL]), locator, timeout)
                for element in elements:
                    element.wait_for = types.MethodType(wait_for, element)
                    element.get_child = types.MethodType(get_element, element)
                    element.get_children = types.MethodType(get_children, element)
                return elements
    raise FTTException("Locator: {} does not start with known by method.".format(coordinate), "Invalid Locator")


def is_available(self, coordinate, timeout=TIMEOUT):
    if isinstance(coordinate, str):
        try:
            return self.get_element(coordinate, timeout)
        except FTTException as e:
            if e.status in ['Not Displayed', 'Not Found']:
                return False
            raise e
    return coordinate.is_displayed()


def wait_for(self, method, locator, timeout=TIMEOUT):
    """Wait until the element specified by the given locator (i.e. string selector) is displayed to the user."""
    status = "Unknown"
    for index in range(timeout):
        try:
            element = method(locator)
            try:
                if element.is_displayed():
                    return element
            # When we get a list of element instead of a single element, we check if any of them is visible
            except AttributeError:
                for _element in element:
                    if _element.is_displayed():
                        return element
            status = "Not Displayed"
        except (NoSuchElementException, StaleElementReferenceException) as e:
            status = "Not Found" if isinstance(e, NoSuchElementException) else "Stale Element"
        self.wait(1)
    raise FTTException("wait_for({}, {}, {}), timeout reached; Status: {}".format(
        method.__name__, locator, timeout, status), status=status)
