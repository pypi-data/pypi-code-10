"""
WebPortfolio

"""
import re
import os
import sys
import inspect
import datetime
import functools
import logging
import logging.config
import utils
from werkzeug.contrib.fixers import ProxyFix
from werkzeug.routing import BaseConverter, parse_rule
from flask import Flask, render_template, flash, session, url_for, request, make_response, Response
from flask_assets import Environment
import jinja2
import __about__


_py2 = sys.version_info[0] == 2
# ------------------------------------------------------------------------------

NAME = __about__.name
__version__ = __about__.version
__author__ = __about__.author
__license__ = __about__.license
__copyright__ = __about__.copyright

# ------------------------------------------------------------------------------

__all__ = ["WebPortfolio",
           "get_env",
           "get_env_config",
           "flash_error",
           "flash_success",
           "flash_info",
           "flash_data",
           "get_flashed_data",
           "route",
           "url_for",
           "init_app",
           "register_package"]

# Env
def get_env():
    """
    Return the Capitalize environment name
    It can be used to retrieve class base config
    Default: Development
    :returns: str
    """
    env_key = "WEBPORTFOLIO_ENV"
    env = "Development"
    if env_key in os.environ:
        env = os.environ[env_key].lower().capitalize()
    return env

def get_env_config(config):
    """
    Return config class
    :param config : Object - The configuration module containing the environment object
    """
    return getattr(config, get_env())

def route(rule, **options):
    """A decorator that is used to define custom routes for methods in
    FlaskView subclasses. The format is exactly the same as Flask's
    `@app.route` decorator.
    """

    def decorator(f):
        # Put the rule cache on the method itself instead of globally
        if not hasattr(f, '_rule_cache') or f._rule_cache is None:
            f._rule_cache = {f.__name__: [(rule, options)]}
        elif not f.__name__ in f._rule_cache:
            f._rule_cache[f.__name__] = [(rule, options)]
        else:
            f._rule_cache[f.__name__].append((rule, options))

        return f

    return decorator

def init_app(kls):
    """
    To bind middlewares that needs the 'app' object to init
    Bound middlewares will be assigned on cls.init()
    """
    if not hasattr(kls, "__call__"):
        raise TypeError("init_app: '%s' is not callable" % kls)
    WebPortfolio._init_apps.add(kls)
    return kls

def register_package(root_pkg=None, template="templates", static="static"):
    """
    Register a package's template directory and static
    :param root_pkg: str - The root dir,
                    or the dotted resource package (package.path.path,
                    usually __name__ of templates and static
    :param template: str - The template dir name. If root_dir is none,
                    template should be a path
    :param static: str - The static dir name. If root_dir is none,
                    static should be a path
    """
    if root_pkg:
        if not os.path.isdir(root_pkg) and "." in root_pkg:
            root_pkg = utils.get_pkg_resources_filename(root_pkg)

        template_path = os.path.join(root_pkg, template)
        static_path = os.path.join(root_pkg, static)
    else:
        template_path = template
        static_path = static

    if os.path.isdir(template_path):
        template_path = jinja2.FileSystemLoader(template_path)
        WebPortfolio._template_paths.add(template_path)
    else:
        logging.warn("Package registration: Not a <template> directory '%s' " % template_path)

    if os.path.isdir(static_path):
        WebPortfolio._static_paths.add(static_path)
        WebPortfolio._add_asset_bundle(static_path)
    else:
        logging.warn("Package registration: Not a <static> directory '%s' " % static_path)

# Flashing
def flash_error(message):
    """ Set an error message """
    flash(message, "error")

def flash_success(message):
    """ Set an success message """
    flash(message, "success")

def flash_info(message):
    """ Set an info message """
    flash(message, "info")

def flash_data(data):
    """
    Just like flash, but will save data
    :param data:
    :return:
    """
    session["_flash_data"] = data

def get_flashed_data():
    """
    Retrieved
    :return: mixed
    """
    return session.pop("_flash_data", None)

# ------------------------------------------------------------------------------

# https://github.com/apiguy/flask-classy
class FlaskView(object):
    """Base view for any class based views implemented with Flask-Classy. Will
    automatically configure routes when registered with a Flask app instance.
    """

    decorators = []
    route_base = None
    route_prefix = None
    trailing_slash = True

    @classmethod
    def register(cls, app, route_base=None, subdomain=None, route_prefix=None,
                 trailing_slash=None):
        """Registers a FlaskView class for use with a specific instance of a
        Flask app. Any methods not prefixes with an underscore are candidates
        to be routed and will have routes registered when this method is
        called.

        :param app: an instance of a Flask application

        :param route_base: The base path to use for all routes registered for
                           this class. Overrides the route_base attribute if
                           it has been set.

        :param subdomain:  A subdomain that this registration should use when
                           configuring routes.

        :param route_prefix: A prefix to be applied to all routes registered
                             for this class. Precedes route_base. Overrides
                             the class' route_prefix if it has been set.
        """

        if cls is FlaskView:
            raise TypeError("cls must be a subclass of FlaskView, not FlaskView itself")

        if route_base:
            cls.orig_route_base = cls.route_base
            cls.route_base = route_base

        if route_prefix:
            cls.orig_route_prefix = cls.route_prefix
            cls.route_prefix = route_prefix

        if not subdomain:
            if hasattr(app, "subdomain") and app.subdomain is not None:
                subdomain = app.subdomain
            elif hasattr(cls, "subdomain"):
                subdomain = cls.subdomain

        if trailing_slash is not None:
            cls.orig_trailing_slash = cls.trailing_slash
            cls.trailing_slash = trailing_slash

        members = get_interesting_members(FlaskView, cls)
        special_methods = ["get", "put", "patch", "post", "delete", "index"]

        for name, value in members:
            proxy = cls.make_proxy_method(name)
            route_name = cls.build_route_name(name)
            try:
                if hasattr(value, "_rule_cache") and name in value._rule_cache:
                    for idx, cached_rule in enumerate(value._rule_cache[name]):
                        rule, options = cached_rule
                        rule = cls.build_rule(rule)
                        sub, ep, options = cls.parse_options(options)

                        if not subdomain and sub:
                            subdomain = sub

                        if ep:
                            endpoint = ep
                        elif len(value._rule_cache[name]) == 1:
                            endpoint = route_name
                        else:
                            endpoint = "%s_%d" % (route_name, idx,)

                        app.add_url_rule(rule, endpoint, proxy, subdomain=subdomain, **options)

                elif name in special_methods:
                    if name in ["get", "index"]:
                        methods = ["GET"]
                    else:
                        methods = [name.upper()]

                    rule = cls.build_rule("/", value)
                    if not cls.trailing_slash:
                        rule = rule.rstrip("/")
                    app.add_url_rule(rule, route_name, proxy, methods=methods, subdomain=subdomain)

                else:
                    name = utils.dasherize(name)
                    route_str = '/%s/' % name
                    if not cls.trailing_slash:
                        route_str = route_str.rstrip('/')
                    rule = cls.build_rule(route_str, value)
                    app.add_url_rule(rule, route_name, proxy, subdomain=subdomain)
            except DecoratorCompatibilityError:
                raise DecoratorCompatibilityError("Incompatible decorator detected on %s in class %s" % (name, cls.__name__))

        if hasattr(cls, "orig_route_base"):
            cls.route_base = cls.orig_route_base
            del cls.orig_route_base

        if hasattr(cls, "orig_route_prefix"):
            cls.route_prefix = cls.orig_route_prefix
            del cls.orig_route_prefix

        if hasattr(cls, "orig_trailing_slash"):
            cls.trailing_slash = cls.orig_trailing_slash
            del cls.orig_trailing_slash

    @classmethod
    def parse_options(cls, options):
        """Extracts subdomain and endpoint values from the options dict and returns
           them along with a new dict without those values.
        """
        options = options.copy()
        subdomain = options.pop('subdomain', None)
        endpoint = options.pop('endpoint', None)
        return subdomain, endpoint, options,

    @classmethod
    def make_proxy_method(cls, name):
        """Creates a proxy function that can be used by Flasks routing. The
        proxy instantiates the FlaskView subclass and calls the appropriate
        method.
        :param name: the name of the method to create a proxy for
        """

        i = cls()
        view = getattr(i, name)

        if cls.decorators:
            for decorator in cls.decorators:
                view = decorator(view)

        @functools.wraps(view)
        def proxy(**forgettable_view_args):
            # Always use the global request object's view_args, because they
            # can be modified by intervening function before an endpoint or
            # wrapper gets called. This matches Flask's behavior.
            del forgettable_view_args

            if hasattr(i, "before_request"):
                response = i.before_request(name, **request.view_args)
                if response is not None:
                    return response

            before_view_name = "before_" + name
            if hasattr(i, before_view_name):
                before_view = getattr(i, before_view_name)
                response = before_view(**request.view_args)
                if response is not None:
                    return response

            response = view(**request.view_args)

            # You can also return a dict, it will pass it to render
            if isinstance(response, dict):
                df_v_t = "%s/%s.html" % (cls.__name__, view.__name__)
                response.setdefault("view_template_", df_v_t)
                response = cls.render_(**response)

            if not isinstance(response, Response):
                response = make_response(response)

            after_view_name = "after_" + name
            if hasattr(i, after_view_name):
                after_view = getattr(i, after_view_name)
                response = after_view(response)

            if hasattr(i, "after_request"):
                response = i.after_request(name, response)

            return response

        return proxy

    @classmethod
    def build_rule(cls, rule, method=None):
        """Creates a routing rule based on either the class name (minus the
        'View' suffix) or the defined `route_base` attribute of the class

        :param rule: the path portion that should be appended to the
                     route base

        :param method: if a method's arguments should be considered when
                       constructing the rule, provide a reference to the
                       method here. arguments named "self" will be ignored
        """

        rule_parts = []

        if cls.route_prefix:
            rule_parts.append(cls.route_prefix)

        route_base = cls.get_route_base()
        if route_base:
            rule_parts.append(route_base)

        rule_parts.append(rule)
        ignored_rule_args = ['self']
        if hasattr(cls, 'base_args'):
            ignored_rule_args += cls.base_args

        if method:
            args = get_true_argspec(method)[0]
            for arg in args:
                if arg not in ignored_rule_args:
                    rule_parts.append("<%s>" % arg)

        result = "/%s" % "/".join(rule_parts)
        return re.sub(r'(/)\1+', r'\1', result)

    @classmethod
    def get_route_base(cls):
        """Returns the route base to use for the current class."""

        if cls.route_base is not None:
            route_base = cls.route_base
            base_rule = parse_rule(route_base)
            cls.base_args = [r[2] for r in base_rule]
        else:
            if cls.__name__.endswith("View"):
                route_base = cls.__name__[:-4].lower()
            else:
                route_base = cls.__name__.lower()

        return route_base.strip("/")

    @classmethod
    def build_route_name(cls, method_name):
        """Creates a unique route name based on the combination of the class
        name with the method name.

        :param method_name: the method name to use when building a route name
        """
        return cls.__name__ + ":%s" % method_name

# WebPorfolio
class WebPortfolio(FlaskView):
    """ WebPortfolio """
    LAYOUT = "layout.html"  # The default layout
    PAGE_META = "PAGE_META"
    GLOBAL_KEY_CONTEXT = "__g"
    assets = None
    _app = None
    _init_apps = set()
    _template_paths = set()
    _static_paths = set()
    _asset_bundles = set()
    _default_page_meta = dict(
            title="",
            description="",
            url="",
            image="",
            site_name="",
            object_type="article",
            locale="",
            keywords=[],
            use_opengraph=True,
            use_googleplus=True,
            use_twitter=True,
            properties={}
        )
    _global = dict(
        WEBPORTFOLIO_NAME=NAME,
        WEBPORTFOLIO_VERSION=__version__,
        YEAR=datetime.datetime.now().year,
        PAGE_META=_default_page_meta
    )

    @classmethod
    def init(cls, flask_or_import_name, project=None, directory=None, config=None,
             compress_html=True):
        """
        Allow to register all subclasses of WebPortfolio at once

        If a class doesn't have a route base, it will create a dasherize version
        of the class name.

        So we call it once initiating
        :param flask_or_import_name: Flask instance or import name -> __name__
        :param project: name of the project. If the directory and config is empty, it will guess them from here
        :param directory: The directory containing your project's Views, Templates and Static
        :param config: string of config object. ie: "app.config.Dev"
        :param compress_html: bool - If true it will use the plugin "jinja2htmlcompress"
                to remove white spaces off the html resul
        """

        if isinstance(flask_or_import_name, Flask):
            app = flask_or_import_name
        else:
            app = Flask(flask_or_import_name)

        app.wsgi_app = ProxyFix(app.wsgi_app)

        app.url_map.converters['regex'] = RegexConverter

        if not directory:
            directory = "application/%s" % project if project else "."

        if not config:
            config = "application.config.%s" % get_env()

        app.config.from_object(config)

        cls._setup_logger(app)

        if directory:
            app.template_folder = directory + "/templates"
            app.static_folder = directory + "/static"

        cls._add_asset_bundle(app.static_folder)

        # Extensions to remove extra white spaces in html
        if compress_html:
            app.jinja_env.add_extension('webportfolio.jinja2htmlcompress.HTMLCompress')

        cls._app = app

        # Flask Assets
        cls.assets = Environment(cls._app)

        # Register templates
        if cls._template_paths:
            loader = [cls._app.jinja_loader] + list(cls._template_paths)
            cls._app.jinja_loader = jinja2.ChoiceLoader(loader)

        # Register static
        if cls._static_paths:
            loader = [cls._app.static_folder] + list(cls._static_paths)
            cls.assets.load_path = loader

        # init_app
        for _app in cls._init_apps:
            _app(cls._app)

        # Register all views
        for subcls in cls.__subclasses__():
            route_base = subcls.route_base
            if not route_base:
                route_base = utils.dasherize(utils.underscore(subcls.__name__))
            subcls.register(cls._app, route_base=route_base)

        # Load all bundles
        [cls.assets.from_yaml(a) for a in cls._asset_bundles]

        @cls._app.after_request
        def _after_request_cleanup(response):
            cls._global["PAGE_META"] = cls._default_page_meta
            cls._global["PAGE_META"]["site_name"] = cls._app.config.get("APPLICATION_NAME", "")
            return response

        return cls._app

    @classmethod
    def render_(cls, data={}, view_template_=None, layout_=None, **kwargs):
        """
        To render data to the associate template file of the action view
        :param data: The context data to pass to the template
        :param view_template_: The file template to use. By default it will map the classname/action.html
        :param layout_: The body layout, must contain {% include __template__ %}
        """
        if not view_template_:
            stack = inspect.stack()[1]
            module = inspect.getmodule(cls).__name__
            module_name = module.split(".")[-1]
            action_name = stack[3]      # The method being called in the class
            view_name = cls.__name__    # The name of the class without View

            if view_name.endswith("View"):
                view_name = view_name[:-4]
            view_template_ = "%s/%s.html" % (view_name, action_name)

        data = data or dict()
        data["__g"] = cls._global
        if kwargs:
            data.update(kwargs)

        data["__template__"] = view_template_

        return render_template(layout_ or cls.LAYOUT, **data)

    @classmethod
    def meta_(cls, **kwargs):
        """
        Meta allows you to add meta data to site
        :params **kwargs:

        meta keys we're expecting:
            title (str)
            description (str)
            url (str) (Will pick it up by itself if not set)
            image (str)
            site_name (str) (but can pick it up from config file)
            object_type (str)
            keywords (list)
            locale (str)
            card (str)

            **Boolean By default these keys are True
            use_opengraph
            use_twitter
            use_googleplus

        """
        n = cls.PAGE_META
        page_meta = cls._global.get(n, {})
        page_meta.update(**kwargs)
        cls.g(n=page_meta)

    @property
    def logger_(self):
        """
        SHortcut to the Flask.logger
        :return:
        """
        return self._app.logger

    @classmethod
    def config_(cls, key, default=None):
        """
        Shortcut to access the config in your class
        :param key: The key to access
        :param default: The default value when None
        :returns mixed:
        """
        return cls._app.config.get(key, default)

    @classmethod
    def g(cls, **kwargs):
        """
        Assign a global view context to be used in the template
        :params **kwargs:
        """
        cls._global.update(kwargs)

    @classmethod
    def nav_menu_context(cls):
        return dict(module_=cls.__module__, class_=cls.__name__)

    @classmethod
    def _add_asset_bundle(cls, path):
        """
        Add a webassets bundle yml file
        """
        f = "%s/assets.yml" % path
        if os.path.isfile(f):
            cls._asset_bundles.add(f)

    @classmethod
    def _extends(cls, kls):
        """
        A view decorator to extend another view class or function to itself
        It will inherit all its methods and propeties and use them on itself

        -- EXAMPLES --

        class Index(WebPortfolio):
            pass

        index = Index()

        ::-> As decorator on classes ::
        @index.extends__
        class A(object):
            def hello(self):
                pass

        @index.extends__
        class C()
            def world(self):
                pass

        ::-> Decorator With function call ::
        @index.extends__
        def hello(self):
            pass

        """
        if inspect.isclass(kls):
            for _name, _val in kls.__dict__.items():
                if not _name.startswith("__"):
                    setattr(cls, _name, _val)
        elif inspect.isfunction(kls):
            setattr(cls, kls.__name__, kls)
        return cls

    @classmethod
    def _setup_logger(cls, app):
        if "LOGGING_CONFIG" in app.config:
            logging.config.dictConfig(app.config["LOGGING_CONFIG"])
            logger = logging.getLogger("root")
            app._logger = logger
            app._loger_name = logger.name

def get_interesting_members(base_class, cls):
    """Returns a list of methods that can be routed to"""

    base_members = dir(base_class)
    predicate = inspect.ismethod if _py2 else inspect.isfunction
    all_members = inspect.getmembers(cls, predicate=predicate)
    return [member for member in all_members
            if not member[0] in base_members
            and ((hasattr(member[1], "__self__") and not member[1].__self__ in inspect.getmro(cls)) if _py2 else True)
            and not member[0].startswith("_")
            and not member[0].startswith("before_")
            and not member[0].startswith("after_")]

def get_true_argspec(method):
    """Drills through layers of decorators attempting to locate the actual argspec for the method."""

    argspec = inspect.getargspec(method)
    args = argspec[0]
    if args and args[0] == 'self':
        return argspec
    if hasattr(method, '__func__'):
        method = method.__func__
    if not hasattr(method, '__closure__') or method.__closure__ is None:
        raise DecoratorCompatibilityError

    closure = method.__closure__
    for cell in closure:
        inner_method = cell.cell_contents
        if inner_method is method:
            continue
        if not inspect.isfunction(inner_method) \
            and not inspect.ismethod(inner_method):
            continue
        true_argspec = get_true_argspec(inner_method)
        if true_argspec:
            return true_argspec

class DecoratorCompatibilityError(Exception):
    pass

class RegexConverter(BaseConverter):
    def __init__(self, url_map, *items):
        super(RegexConverter, self).__init__(url_map)
        self.regex = items[0]
