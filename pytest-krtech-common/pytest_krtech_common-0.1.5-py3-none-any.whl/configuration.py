# coding=utf-8

from urllib.parse import urljoin
from allure.constants import AttachmentType
from selenium import webdriver
import allure


class TestConfig:
    driver = None
    base_url = "http://127.0.0.1"
    element_wait = 5
    page_load_timeout = 20
    element_init_timeout = 0.1
    mysqlhost = "127.0.0.1"
    mysqluser = "root"
    mysqlpassword = "toor"
    mysqldb = "dbname"


class BaseUrlWrapper(webdriver.Remote):
    def __init__(self, base, *args, **kwargs):
        self._base_url = base
        super(BaseUrlWrapper, self).__init__(*args, **kwargs)

    def get(self, url='/'):
        url = urljoin(self._base_url, url)
        return super(BaseUrlWrapper, self).get(url)


class ConftestOptions:
    def __init__(self, testconf):
        self.testconf = testconf

    def pytest_runtest_makereport(self, item, call, __multicall__):
        report = __multicall__.execute()

        if report.when in ('call', 'teardown') and report.failed:
            attrs = getattr(item, 'funcargs')
            driver = attrs['config'].driver
            allure.attach('screenshot', driver.get_screenshot_as_png(), type=AttachmentType.PNG)

        return report

    def pytest_addoption(self, parser):
        parser.addoption("--base_url", action="store", default=self.testconf.base_url)
        parser.addoption("--browser", action="store", default="firefox")
        parser.addoption("--element_wait", action="store", default=self.testconf.element_wait)
        parser.addoption("--page_load_timeout", action="store", default=self.testconf.page_load_timeout)
        parser.addoption("--element_init_timeout", action="store", default=self.testconf.element_init_timeout)
        return parser

    def config(self, request):
        driver_ = BaseUrlWrapper(
            base=self.testconf.base_url,
            desired_capabilities={'browserName': request.config.option.browser}
        )

        driver_.maximize_window()
        driver_.set_page_load_timeout(request.config.option.page_load_timeout)

        self.testconf.driver = driver_
        self.testconf.base_url = request.config.option.base_url

        return self.testconf
