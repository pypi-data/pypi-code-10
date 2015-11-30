# -*- coding: utf-8 -*-
"""
    ghostly.ghostly
    ~~~~~~~~~~~~~~~

    Lightweight wrapper and helpers around Selenium Webdriver.

"""
from __future__ import absolute_import, print_function, unicode_literals
import time

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import ActionChains

from .errors import DriverDoesNotExistError, GhostlyTestFailed, \
    GhostlyTimeoutError


class Ghostly:
    """
    Lightweight wrapper and helper utilities around Selenium webdriver.
    """

    def __init__(self, driver, maximise_window=True):
        """
        :param driver: String name of driver, it's expected that it's an attribute
                       on webdriver. IE. 'Chrome' or 'Firefox' are valid.
        """

        try:
            self.driver = getattr(webdriver, driver)()
            """:type : webdriver.Chrome"""
        except AttributeError as e:
            raise DriverDoesNotExistError("Driver '%s' does not exist." % driver)

        if maximise_window:
            self.driver.maximize_window()

    def end(self):
        self.driver.quit()

    def get(self, url):
        """
        Load the provided URL in the web driver
        """
        return self.driver.get(url)

    def xpath_click(self, xpath, wait=0.1, move_to=True):
        """
        Click an element selected using xpath.

        :param xpath: The xpath locator of the element to be clicked.
        :param wait: Wait after the click - set to None for no wait.
        :param move_to: If True (default) then an ActionChains is created and
                        move_to_element called - this approach works well for
                        elements that respond to clicks such as a/span/div tags.
                        If False, click is called on the element - this approach
                        works well for choosing items in a select tag.
        """
        element = self.xpath(xpath)

        if move_to:
            ActionChains(self.driver)\
                .move_to_element(element)\
                .click()\
                .perform()
        else:
            element.click()

        if wait is not None:
            self.wait(wait)

    def xpath_wait(self, xpath, visible=True, timeout=5, sleep=0.25):
        """
        Wait for timeout seconds for xpath to exist and optionally be visible.

        :param xpath: The xpath locator of the element to find.
        :param visible: If True, also wait for the element to become visible.
        :param timeout: Timeout in seconds before GhostlyTimeoutError is raised.
        :param sleep: How long to sleep for between each check to see if
        :return: selenium.webdriver.remote.webelement.WebElement
        """
        start = current = time.time()
        stop = start + timeout
        attempts = 0

        # Initially wait till the element can be found
        while time.time() < stop:
            attempts += 1
            # We haven't yet found the element
            try:
                # Attempt to select the element.
                element = self.xpath(xpath)
                break
            except NoSuchElementException:
                # The element isn't available yet, so wait.
                self.wait(sleep)
        else:
            raise GhostlyTimeoutError(
                "Could not select xpath '%s' within %s seconds - attempted %s "
                "times." % (xpath, timeout, attempts)
            )

        if not visible:
            return element

        # Wait till it's visible
        while time.time() < stop:
            attempts += 1
            if element.is_displayed():
                return element
            else:
                # The element isn't displayed, wait
                self.wait(sleep)
        else:
            raise GhostlyTimeoutError(
                "Element selected via xpath '%s' but is not yet visible within %s seconds - attempted %s "
                "times." % (xpath, timeout, attempts)
            )

    def xpath(self, xpath):
        """
        Finds an element by xpath.

        This simply passes through to
        :py:class:`.WebDriver.find_element_by_xpath`.

        :param xpath: The xpath locator of the element to find.
        :return: selenium.webdriver.remote.webelement.WebElement
        """
        return self.driver.find_element_by_xpath(xpath)

    def wait(self, seconds):
        """
        Wait for a specified number of seconds
        """
        if type(seconds) == str:
            seconds = int(seconds)
        time.sleep(seconds)

    def form_submit(self, xpath, **data):
        """
        Submit a form optionally setting (simple) data on the form.

        :param xpath: The xpath locator of the form.
        :param data: A dict of data to supply to :py:meth:`.Ghostly.form_fill`
        :return: selenium.webdriver.remote.webelement.WebElement
        """
        form = self.form_fill(xpath, **data)
        return form.submit()

    def form_fill(self, xpath, **data):
        """
        Fill a simple form with data.

        :param xpath: The xpath locator of the form.
        :param data: A dict of data on the form to fill. The key of each item
                     should equal the name of an input field.
        :return: selenium.webdriver.remote.webelement.WebElement
        """
        form = self.xpath(xpath)
        for field, value in data.items():
            self.xpath(xpath + '//*[@name="' + field + '"]').send_keys(value)

        return form
