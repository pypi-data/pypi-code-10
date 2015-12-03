import functools
import inspect
from flask import Response, jsonify, abort, request, current_app
from werkzeug.wrappers import BaseResponse
from core import WebPortfolio, init_app
from dicttoxml import dicttoxml
import ext

__all__ = [
    "extends",
    "render_as_json",
    "render_as_xml",
    "nav_menu",
    "nav_menu_add",
    "with_user_roles",
    "login_required",
    "no_login_required",
]
# ------------------------------------------------------------------------------
def extends(module, *args, **kwargs):
    """
    Decorator to extend a module to a view.
    The module can be a class or function. It will copy all the methods to the class

    ie:
        #Your module.py
        welcome_module(view, **kwargs):

            @route("/welcome-home")
            my_view():
                pass
            return my_view

        #Your view.py
        @extends(welcome_module)
        class Index(WebPortfolio):
            pass

    :param module: object
    :param args:
    :param kwargs:
    :return:
    """
    def wrap(view):
        return view._extends(module(view, *args, **kwargs))
    return wrap

# ------------------------------------------------------------------------------
"""
VIEW RENDERING DECORATORS

It allows you quickly switch the rendering view of a method.
For it to work all methods must return a dict. Even empty.
By default it will render the page as template


    class Index(WebPortfolio):

        @render_as_json
        def index2():
            retun {}

        @render_as_xml
        def index():
            retun {}

"""
# Helper function to normalize view return values .
# It always returns (dict, status, headers). Missing values will be None.
# For example in such cases when tuple_ is
#   (dict, status), (dict, headers), (dict, status, headers),
#   (dict, headers, status)
#
# It assumes what status is int, so this construction will not work:
# (dict, None, headers) - it doesn't make sense because you just use
# (dict, headers) if you want to skip status.
def _normalize_response_tuple(tuple_):
    v = tuple_ + (None,) * (3 - len(tuple_))
    return v if isinstance(v[1], int) else (v[0], v[2], v[1])


# Helper function to create JSON response for the given data.
# Raises an error if the data is not convertible to JSON.
def _build_response(data, renderer=None):
    if isinstance(data, Response) or isinstance(data, BaseResponse):
        return data
    if not renderer:
        raise AttributeError(" Renderer is required")
    if isinstance(data, dict):
        return renderer(data), 200
    elif isinstance(data, tuple):
        data, status, headers = _normalize_response_tuple(data)
        return renderer(data or {}), status, headers
    else:
        raise ValueError('Unsupported return value.')

def render_as_json(func):
    """
    Decorator to render as JSON
    :param func:
    :return:
    """
    @functools.wraps(func)
    def decorated_view(*args, **kwargs):
        data = func(*args, **kwargs)
        return _build_response(data, jsonify)
    return decorated_view

def render_as_xml(func):
    """
    Decorator to render as XML
    :param func:
    :return:
    """
    @functools.wraps(func)
    def decorated_view(*args, **kwargs):
        data = func(*args, **kwargs)
        return _build_response(data, dicttoxml)
    return decorated_view


# ------------------------------------------------------------------------------
#
# @nav_menu
#
# Decorator to build navigation menu directly from the methods
# By default it will build the menu of the module, class an method
# If the class is also decorated, it will use the menu name as the top
# level name

_NAV_MENU_STACK = {}

def nav_menu_add(name, module_, class_, method_=None, is_class_=False, **kwargs):
    """
    To manually add nav menu
    :param name:
    :param module_:
    :param class_:
    :param method_:
    :param is_class_:
    :param kwargs:
    :return:
    """
    _push_nav_menu(module_=module_,
                   class_=class_,
                   method_=method_,
                   is_class_=is_class_,
                   name=name,
                   **kwargs)

def nav_menu(name, **kwargs):
    """
    Decorator to build navigation menu directly on the methods
    By default it will build the menu of the module, class an method
    If the class is also decorated, it will use the menu name as the top level name

    :param name: The menu name
    :param kwargs: extra options to pass into the menu or to move the menu somewhere else

        order int: The order of the menu in the set

        show (list of bool or callback): To hide and show menu. Accepts bool or
                    list of callback function the callback function must return
                    a bool to check if all everything is True to show or will be False
                    ** When this menu is inside of a menu set, or has parent, if you want
                    that page to be activated, but don't want to create a menu link,
                    for example: a blog read page, set show to False. It will know
                    the menu set is active

        endpoint string: By default the endpoint is built based on the method and class.
                    When set it will be used instead

        endpoint_kwargs dict: dict of k/v data for enpoint

        group: On class menu, it can be used to filter a menu set to display

        The args below will allow you to change where the menu is placed.
        By default they are set automatically

        module_: the module name. Usually if using another module
        class_: the class name class name in the module
        method_: The method name, to build endpoint. Changing this will cha
        is_class_: When the decorator is on the class instead of the method.
            This will be used to make the top level.
            Function not inside of class, may say it's a class, set is_class_ = False

    :return:
    """
    def wrap(f):
        if name is not None:
            module_ = kwargs.pop("module_", f.__module__)
            class_ = kwargs.pop("class_", inspect.stack()[1][3])
            is_class_ = kwargs.pop("is_class_", inspect.isclass(f))
            method_ = kwargs.pop("method_", f.__name__)

            _push_nav_menu(module_=module_,
                           class_=class_,
                           method_=method_,
                           is_class_=is_class_,
                           name=name,
                           **kwargs)

        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            return f(*args, **kwargs)
        return wrapper
    return wrap

def _push_nav_menu(**kwargs):

    module_ = kwargs.pop("module_")
    class_ = kwargs.pop("class_")
    method_ = kwargs.pop("method_")
    is_class_ = kwargs.pop("is_class_")

    __cls = method_ if is_class_ else class_
    path = "%s.%s" % (module_, __cls)

    if path not in _NAV_MENU_STACK:
        _NAV_MENU_STACK[path] = {
            "name": None,
            "endpoint": None,
            "endpoint_kwargs": {},
            "order": None,
            "sub_menu": [],
            "kwargs": {}
        }

    if "name" not in kwargs:
        raise TypeError("Missing 'name' in menu decorator")

    kwargs["endpoint"] = kwargs.pop("endpoint", "%s:%s" % (__cls,
                                                         "index" if is_class_ else method_ ))
    kwargs["endpoint_kwargs"] = kwargs.pop("endpoint_kwargs", {})
    order = kwargs.pop("order", 0)
    name = kwargs.pop("name")
    endpoint = kwargs.pop("endpoint")

    # show: accepts a bool or list of callback to execute
    show = kwargs.pop("show", [])

    if isinstance(show, bool):
        show = [show]
    elif show and not isinstance(show, list):
        show = [show]

    kwargs["show"] = show
    kwargs["__active"] = None
    kwargs["__index"] = None

    if is_class_:  # class menu
        kwargs["endpoint"] = endpoint
        kwargs["group"] = kwargs.pop("group", None)
        _NAV_MENU_STACK[path]["name"] = name
        _NAV_MENU_STACK[path]["order"] = order
        _NAV_MENU_STACK[path]["kwargs"] = kwargs
    else:  # sub menu
        menu = (order, name, endpoint, kwargs)
        _NAV_MENU_STACK[path]["sub_menu"].append(menu)

def _nav_menu_test_show(shows):
    return all([x() if hasattr(x, "__call__") else x for x in shows])

def _nav_menu_init(app):
    @app.before_request
    def p(*args, **kwargs):

        # (order, Name, sub_menu, **kargs, hidden_submenu)
        menu_list = []
        menu_index = 0
        for _, menu in _NAV_MENU_STACK.items():
            menu_index += 1

            menu["kwargs"]["__index"] = menu_index
            menu["kwargs"]["__active"] = False

            # Filter out menu that should not be shown
            _kw = menu["kwargs"]
            if _kw and "show" in _kw and _nav_menu_test_show(_kw["show"]) is False:
                continue

            sub_menu = []
            sub_menu_hidden = []  # Save all the hidden submenu

            for s in menu["sub_menu"]:
                if s[2] == request.endpoint:
                    s[3]["__active"] = True
                    menu["kwargs"]["__active"] = True

                sub_menu_hidden.append(s)

                _kw = s[3]
                if _kw and "show" in _kw and _nav_menu_test_show(_kw["show"]) is False:
                    continue
                sub_menu.append(s)

            _kwargs = menu["kwargs"]
            _kwargs["__hidden"] = sorted(sub_menu_hidden)
            menu_list.append((
                menu["order"],
                menu["name"],
                sorted(sub_menu),
                _kwargs
            ))

        WebPortfolio.g(NAV_MENU=sorted(menu_list))

init_app(_nav_menu_init)

# ------------------------------------------------------------------------------

def with_user_roles(*roles):
    """
    A decorator to check if user has any of the roles specified

    @with_user_roles('superadmin', 'admin')
    def fn():
        pass
    """
    def wrapper(f):
        @functools.wraps(f)
        def wrapped(*args, **kwargs):
            if ext.user_authenticated():
                if not ext.flask_login.current_user.has_any_roles(*roles):
                    return abort(403)
            else:
                return abort(401)
            return f(*args, **kwargs)
        return wrapped
    return wrapper

def with_user_permissions(*permissions):
    pass

def login_required(func):
    """
    A wrapper around the flask_login.login_required.
    But it also checks the presence of the decorator: @no_login_required
    On a "@login_required" class, method containing "@no_login_required" will
    still be able to access without authentication
    :param func:
    :return:
    """
    @functools.wraps(func)
    def decorated_view(*args, **kwargs):
        if "no_login_required" not in ext.utils.get_decorators_list(func) \
                and ext.user_not_authenticated():
            return current_app.login_manager.unauthorized()
        return func(*args, **kwargs)
    return decorated_view

def no_login_required(func):
    """
    Dummy decorator. @login_required will inspect the method
    to look for this decorator
    Use this decorator when you want do not require login in a "@login_required" class/method
    :param func:
    :return:
    """
    @functools.wraps(func)
    def decorated_view(*args, **kwargs):
        return func(*args, **kwargs)
    return decorated_view
