from selenium.webdriver.common.keys import Keys


def kb_type(self, locator, text, clear=None):
    element = self.get_element(locator)
    element.click()
    element.clear()
    if clear is not None:
        for _ in range(clear):
            element.send_keys(Keys.ARROW_RIGHT)
            element.send_keys(Keys.BACKSPACE)
    element.send_keys(text)
