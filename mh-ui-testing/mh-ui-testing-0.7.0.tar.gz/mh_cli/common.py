
import re
import click
import socket
from unipath import Path
from fabric.api import env
from functools import wraps
from urlparse import urljoin
from selenium import webdriver
from mh_pages.pages import LoginPage
from click.exceptions import UsageError
from fabric.contrib.files import exists as remote_exists

OPSWORKS_INBOX_PATH = '/var/matterhorn/inbox'
EC2_INBOX_PATH = '/home/data/opencast/inbox'

class ClickState(object):

    def __init__(self):
        self.username = None
        self.password = None
        self.driver = None
        self.inbox_path = None
        self.host = None
        self.user = None

    @property
    def base_url(self):
        return 'http://' + self.host + '/'

    @property
    def inbox(self):
        if self.inbox_path is not None:
            return self.inbox_path
        if remote_exists(OPSWORKS_INBOX_PATH):
            return OPSWORKS_INBOX_PATH
        elif remote_exists(EC2_INBOX_PATH):
            return EC2_INBOX_PATH
        else:
            raise UsageError("Can't determine remote inbox path")

    @property
    def inbox_dest(self):
        return Path(self.inbox).parent.child('files','collection','inbox')

pass_state = click.make_pass_decorator(ClickState, ensure=True)

def common_callback(ctx, option, value):
    state = ctx.ensure_object(ClickState)
    setattr(state, option.name, value)
    return value

def host_callback(ctx, option, value):
    state = ctx.ensure_object(ClickState)
    if value is not None:
        setattr(state, 'host', socket.gethostbyaddr(value)[0])
    return value

def password_option(f):
    return click.option('-p','--password',
                        expose_value=False,
                        prompt=True,
                        help='MH admin login password',
                        callback=common_callback)(f)

def username_option(f):
    return click.option('-u','--username',
                        expose_value=False,
                        prompt=True,
                        help='MH admin login username',
                        callback=common_callback)(f)

def user_option(f):
    return click.option('-u','--user',
                        expose_value=False,
                        help='The user to execute remote tasks as',
                        callback=common_callback)(f)

def host_option(f):
    return click.option('-H','--host',
                        expose_value=False,
                        help='host/ip of remote admin node',
                        callback=host_callback)(f)

def inbox_path_option(f):
    return click.option('-i', '--inbox_path',
                        expose_value=False,
                        help='alternate path to recording inbox',
                        callback=common_callback)(f)

def selenium_options(f):
    f = password_option(f)
    f = username_option(f)
    f = host_option(f)
    return f

def inbox_options(f):
    f = host_option(f)
    f = user_option(f)
    f = inbox_path_option(f)
    return f

def init_fabric(click_cmd):
    @wraps(click_cmd)
    def wrapped(state, *args, **kwargs):

        # set up the fabric env
        env.host_string = state.host
        if state.user is not None:
            env.user = state.user

        return click_cmd(state, *args, **kwargs)
    return wrapped

def init_driver(init_path=''):
    def decorator(click_cmd):
        @wraps(click_cmd)
        def _wrapped_cmd(state, *args, **kwargs):

            state.driver = webdriver.Firefox()
            state.driver.implicitly_wait(10)
            state.driver.get(urljoin(state.base_url, init_path))

            if 'Login' in state.driver.title:
                page = LoginPage(state.driver)
                page.login(state.username, state.password)

            result = click_cmd(state, *args, **kwargs)

            state.driver.close()
            state.driver.quit()

            return result

        return _wrapped_cmd
    return decorator
