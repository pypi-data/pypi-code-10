from selenium.common.exceptions import NoSuchElementException
from time import sleep

# FYI: Might need to adjust this for Python 3 compatibility
from urlparse import urlparse
import posixpath

# HACK: This is used when dealing w/ long page loads
DELAY = 10


class LoginPage(object):
    """
    Encapsulates the logic for the login page.
    """
    url = "https://www.pinterest.com/login/"

    def __init__(self, session):
        self.session = session

    @property
    def username_field(self):
        return self.session.find_element_by_name("username_or_email")

    @property
    def username(self):
        return self.username_field.get_attribute("value")

    @username.setter
    def username(self, value):
        self.username_field.clear()
        self.username_field.send_keys(value)

    @property
    def password_field(self):
        return self.session.find_element_by_name("password")

    @property
    def password(self):
        return self.password_field.get_attribute("value")

    @password.setter
    def password(self, value):
        self.password_field.clear()
        self.password_field.send_keys(value)

    @property
    def login_button(self):
        return self.session.find_element_by_css_selector("button[type='submit']")

    def submit(self):
        self.login_button.click()

    def authenticate(self, username, password):
        self.username = username
        self.password = password
        self.submit()


class SearchPage(object):
    def __init__(self, session):
        self.session = session

    @property
    def search_field(self):
        return self.session.find_element_by_name("q")

    def search_for(self, *terms):
        sf = self.search_field
        sf.clear()
        sf.send_keys(" ".join(terms) + "\n")

    def load_more_pins(self):
        self.session.execute_script("scroll(0, document.body.scrollHeight);")

        # HACK: Give the page plenty of time to load
        sleep(DELAY)
        return self

    def get_pins_query(self, offset=1, limit=None):
        query = ["//div[contains(@class, 'item')"]
        if offset > 0:
            query.append(" and position() >= %i" % (offset + 1, ))

        if limit:
            query.append(" and position() < %i" % (offset + limit + 1, ))

        query.append("]")
        return ''.join(query)

    def get_pin_elements(self, *args, **kwargs):
        query = self.get_pins_query(*args, **kwargs)
        return self.session.find_elements_by_xpath(query)

    def get_pins(self, *args, **kwargs):
        return [Pin(e) for e in self.get_pin_elements(*args, **kwargs)]


def text_for(element):
    return element.text if element else None


def extract_pin_id(url):
    parsed = urlparse(url)
    path = posixpath.normpath(parsed.path)
    components = path.split(posixpath.sep)
    if components:
        return components[-1]


class Pin(object):
    def __init__(self, base):
        self.base = base

    def get_css(self, query):
        try:
            return self.base.find_element_by_css_selector(query)
        except NoSuchElementException:
            return None

    @property
    def pinterest_link_element(self):
        return self.get_css(".pinImageWrapper")

    @property
    def pinterest_url(self):
        u = self.pinterest_link_element
        return u.get_attribute('href') if u else None

    @property
    def pin_id(self):
        u = self.pinterest_url
        return extract_pin_id(u) if u else None

    @property
    def site_link_element(self):
        return self.get_css(".pinNavLink")

    @property
    def site_url(self):
        s = self.site_link_element
        return s.get_attribute('href') if s else None

    @property
    def image_element(self):
        return self.get_css(".pinImg")

    @property
    def image_url(self):
        i = self.image_element
        return i.get_attribute("src") if i else None

    @property
    def title_element(self):
        return self.get_css(".richPinGridTitle")

    @property
    def title(self):
        return text_for(self.title_element)

    @property
    def description_element(self):
        return self.get_css(".pinDescription")

    @property
    def description(self):
        return text_for(self.description_element)

    @property
    def repin_count_element(self):
        return self.get_css(".repinCountSmall")

    @property
    def repin_count(self):
        c = self.repin_count_element
        return int(c.text) if c else 0

    @property
    def like_count_element(self):
        return self.get_css(".likeCountSmall")

    @property
    def like_count(self):
        c = self.like_count_element
        return int(c.text) if c else 0

    @property
    def comment_count_element(self):
        return self.get_css(".commentCountSmall")

    @property
    def comment_count(self):
        c = self.comment_count_element
        return int(c.text) if c else 0

