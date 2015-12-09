# coding=utf-8
import time

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait


class BasePage(object):
    def __init__(self, config):
        self.__config = config
        self.__name = None
        self.__by = None
        self.__locator = None
        self.__element = None

    @property
    def config(self):
        return self.__config

    @property
    def element(self):
        driver = self.config.driver
        timeout = self.config.element_wait
        time.sleep(self.config.element_init_timeout)
        try:
            WebDriverWait(driver, timeout).until(lambda s: driver.find_element(self.by, self.locator))
            self.__element = self.config.driver.find_element(self.by, self.locator)
        except TimeoutException:
            pass
        return self.__element

    @property
    def locator(self):
        return self.__locator

    @locator.setter
    def locator(self, value):
        self.__locator = value

    @property
    def by(self):
        return self.__by

    @by.setter
    def by(self, value):
        self.__by = value

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        self.__name = value

    def __getitem__(self):
        return self

    def __str__(self):
        return self.name
