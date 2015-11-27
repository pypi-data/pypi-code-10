from selenium.webdriver.common.keys import Keys


def kb_type(self, coordinate, text, clear=None):
    if isinstance(coordinate, str):
        element = self.get_element(coordinate)
    else:
        element = coordinate
    element.click()
    element.clear()
    if clear is not None:
        for _ in range(clear):
            element.send_keys(Keys.ARROW_RIGHT)
            element.send_keys(Keys.BACKSPACE)
    element.send_keys(text)
