import inspect
import pydoc

__author__ = 'umairghani'


class SimpleTCPDispatcher(object):
    """
    Mix-in class that dispatches TCP requests.

    This class is used to register TCP method handlers
    and then to dispatch them. This class doesn't need to be
    instanced directly when used by SimpleTCPServer.
    """

    def __init__(self):
        """
        :constructor:
        :param self
        """
        self.functions = self._register_internal_functions()
        self.instance = None

    def register_instance(self, instance):
        """
        :param instance
        Registers an instance to respond to requests
        """
        self.instance = instance

    def _register_internal_functions(self):
        """
        Registers all the internal functions
        :return: functions dictionary
        """
        return {
            "list_methods": self.list_methods,
            "method_signature": self.method_signature,
            "method_help": self.method_help
        }

    def register_function(self, function, name=None):
        """
        :param function, name (optional)
        Registers a function to respond to requests
        """
        if name is None:
            name = function.__name__

        if name not in self.functions.keys():
            self.functions[name] = function

    def list_methods(self):
        """
        :param self
        :return: Returns a list of methods supported by the server
        """
        methods = self.functions.keys()
        methods.sort()
        return methods

    def method_signature(self, method_name):
        """
        :param method_name
        :return: Returns a list describing the signature of the method.
        """
        if method_name in self.functions.keys():
            _function = self.functions[method_name]
            if inspect.ismethod(_function) or inspect.isfunction(_function):
                _sig = inspect.getargspec(_function)
                _arguments = _sig.args
                # incase it shows self in the signature
                if 'self' in _arguments: _arguments.remove('self')
                return {method_name: _arguments}
            else:
                return {method_name: "Not a proper function/method"}
        else:
            return {method_name: "method/function not found"}

    def method_help(self, method_name):
        """
        :param method_name:
        :return: Returns a string containing documentation of
        the specified method.
        """
        if method_name in self.functions:
            method = self.functions[method_name]
            return pydoc.getdoc(method)
        else:
            return "Method [%s] not found" % method_name

    def _resolve_attributes(self, attr):
        """
        Resolves a dotted attribute name to an object.
        (a, 'b.c.d') => a.b.c.d
        :param attr:
        :return: self.instance
        """
        _attrs = attr.split('.')
        for i in _attrs:
            if i.startswith('_'):
                continue
            else:
                self.instance = getattr(self.instance, i)

        return self.instance

    def _dispatch(self, method, params):
        """
        Dispatches the proper method
        :param method:
        :param params:
        :return: return a json value
        """
        func = None
        try:
            func = self.functions[method]
        except KeyError:
            if self.instance is not None:
                # check for a _dispatch method
                if hasattr(self.instance, '_dispatch'):
                    return self.instance._dispatch(method, params)
                else:
                    # call instance method directly
                    func = self._resolve_attributes(method)

        if func is not None:
            if isinstance(params, list):
                return func(*params)
            elif isinstance(params, dict):
                return func(**params)
            elif params:
                return func(params)
            else:
                return func()
        else:
            raise NameError("method [%s] is not supported" % method)
