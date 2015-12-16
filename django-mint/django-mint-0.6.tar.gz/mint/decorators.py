from mint import exceptions


def get(func):
    def wrapper(self):
        if self.request.method != "GET":
            raise exceptions.HttpNotAllowed("This action needs to be a HTTP GET.")
        return func(self)
    return wrapper


def post(func):
    def wrapper(self):
        if self.request.method != "POST":
            raise exceptions.HttpNotAllowed("This action needs to be a HTTP POST.")
        return func(self)
    return wrapper


def put(func):
    def wrapper(self):
        if self.request.method != "PUT":
            raise exceptions.HttpNotAllowed("This action needs to be a HTTP PUT.")
        return func(self)
    return wrapper


def delete(func):
    def wrapper(self):
        if self.request.method != "DELETE":
            raise exceptions.HttpNotAllowed("This action needs to be a HTTP DELETE.")
        return func(self)
    return wrapper


def requires_id(func):
    def wrapper(self):
        if hasattr(self, 'id') and self.id is None:
            raise exceptions.HttpBadRequest("This action requires an ID")
        return func(self)
    return wrapper


def requires(**kwargs):
    def decorator(function):
        def wrapper(self):
            for arg, typex in kwargs.items():
                if not arg in self.args.keys():
                    raise exceptions.HttpBadRequest("This action requires argument '%s' but it was not passed in." % arg)
                try:
                    if typex == 'string':
                        str(self.args[arg])
                    elif typex == 'integer':
                        int(self.args[arg])
                    elif typex == 'bool':
                        bool(self.args[arg])
                    elif typex == 'float':
                        float(self.args[arg])
                    elif typex == 'tuple':
                        if type(self.args[arg]) in (tuple, list):
                            break
                        else:
                            raise exceptions.HttpBadRequest("This action requires argument '%s' to be a tuple or a list, but checking failed." % arg)
                    elif typex == 'dict':
                        if type(self.args[arg]) == dict:
                            break
                        else:
                            raise exceptions.HttpBadRequest("This action requires argument '%s' to be a dict, but checking failed." % str(arg))
                except ValueError:
                    raise exceptions.HttpBadRequest("This action requires argument '%s' to be a '%s', but a conversion failed." % (arg, typex))
            return function(self)
        return wrapper
    return decorator