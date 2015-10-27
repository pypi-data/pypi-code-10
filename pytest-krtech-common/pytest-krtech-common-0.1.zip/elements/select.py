# coding = utf-8

from elements.base_element import BaseElement
from selenium.webdriver.support.ui import Select as Select_


class Select(BaseElement):

    @property
    def select(self):
        return Select_(self.element)
