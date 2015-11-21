def accept_alert(self):
    if self.name == 'phantomjs':
        # http://stackoverflow.com/questions/15708518/how-can-i-handle-an-alert-with-ghostdriver-via-python
        self.execute_script("window.confirm = function(){return true;}")
    else:
        self.switch_to.alert.accept()


def get_url(self, url):
    if not url:
        print("URL can not be empty or None. Given: {}".format(url))
        assert url
    self.get(url)
    if self.name == 'internet explorer':
        self.press_available("css=a#overridelink")


def iexplorer_wait(self, seconds):
    # TODO: This is a temporary workaround until we figure out
    # how to make iexplorer wait for page to load completely before performing operations
    if self.name == 'internet explorer':
        self.wait(seconds)


def scroll(self, coordinate):
    if isinstance(coordinate, str):
        element = self.get_element(coordinate)
    else:
        element = coordinate
    self.execute_script("arguments[0].scrollIntoView(true);", element)