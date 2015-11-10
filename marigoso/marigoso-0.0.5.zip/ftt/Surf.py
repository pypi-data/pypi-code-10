def accept_alert(self):
    if self.capabilities['browserName'] == 'phantomjs':
        # http://stackoverflow.com/questions/15708518/how-can-i-handle-an-alert-with-ghostdriver-via-python
        self.execute_script("window.confirm = function(){return true;}")
    else:
        self.switch_to.alert.accept()


def get_url(self, url):
    self.get(url)
    if self.capabilities['browserName'] == 'internet explorer':
        self.press_available("css=a#overridelink")




