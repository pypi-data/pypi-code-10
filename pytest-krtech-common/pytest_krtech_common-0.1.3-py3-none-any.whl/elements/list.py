# coding=utf-8
import time

from selenium.webdriver.support.wait import WebDriverWait

from krtech.elements.base_element import BaseElement


class List(BaseElement):

    def __init__(self, name, by, locator):
        super(List, self).__init__(name, by, locator)
        self._elements = []

    def get_element_by_text(self, text):
        for e in self._elements:
            if text in e.text:
                self._element = e
                return self

    @property
    def elements(self):
        return self._elements

    @elements.setter
    def elements(self, value):
        self._elements = value

    def __getitem__(self):
        return self

    def __str__(self):
        return self.name

    def __get__(self, obj, owner):
        driver = obj.driver
        timeout = obj.element_wait
        time.sleep(obj.element_init_timeout)

        WebDriverWait(driver, timeout).until(
            lambda s: len(driver.find_elements(self.by, self.locator)) != 0)
        self._elements = driver.find_elements(self.by, self.locator)
        return self
