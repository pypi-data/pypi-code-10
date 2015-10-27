# coding=utf-8
import time

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait


class BaseElement(object):

    def __init__(self, name, by, locator):
        self.name = name
        self.by = by
        self.locator = locator
        self._element = None

    @property
    def element(self):
        return self._element

    @element.setter
    def element(self, value):
        self._element = value

    def __getitem__(self):
        return self

    def __str__(self):
        return self.name

    def __get__(self, obj, owner):
        driver = obj.driver
        timeout = obj.element_wait

        time.sleep(obj.element_init_timeout)

        try:
            WebDriverWait(driver, timeout).until(
                lambda s: driver.find_element(self.by, self.locator))
            self._element = driver.find_element(self.by, self.locator)
            return self
        except TimeoutException:
            self._element = None
            return self
