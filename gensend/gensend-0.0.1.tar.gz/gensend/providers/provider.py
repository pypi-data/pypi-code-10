import os
from random import Random


class Provider(object):
    def __init__(self):
        self.random = Random()

    def seed(self, seed):
        self.random.seed(seed)

    def _arg_defaults(self, in_args, def_args, factory=None):
        return self._arg_factory(
            factory, [in_args[i] if len(in_args) > i else v for i, v in enumerate(def_args)])

    def _arg_factory(self, factory, args):
        return map(factory, args) if factory else args

    def _wrap_func(self, wrapped, arg_factory=None):
        def wrapper(*args):
            try:
                return wrapped(*self._arg_factory(arg_factory, args))
            except Exception, err:
                return '(FAIL: wrapped func "' + str(wrapped) + '" said ' + str(err) + ')'
        return wrapper

    def _bind_func(self, src_object, attr_name, arg_factory=None):
        return self._wrap_func(getattr(src_object, attr_name), arg_factory)


class ProviderAccessor(object):
    def __init__(self, provider_list=None):
        self.provider_list = ProviderList()

    def call_provider(self, ident, args):
        return self.provider_list.call_provider(ident, args)

    def make_provider_func(self, ident, args):
        return self.provider_list.make_provider_func(ident, args)

    def add_provider(self, provider):
        self.provider_list.append(provider)

    def seed_providers(self, seed):
        self.provider_list.seed_providers(seed)

    def add_providers(self, provider_list):
        for provider in provider_list:
            self.add_provider(provider)


class ProviderList(list):

    @classmethod
    def from_str(cls, provider_str):
        if provider_str.endswith('.py'):
            return cls.from_path(provider_str)
        else:
            return cls.from_module(provider_str)

    @classmethod
    def from_path(cls, provider_str):
        locals_dict = {}
        execfile(os.path.abspath(provider_str), {}, locals_dict)

        return cls.from_mixed_type_list(
            [local_value for local_name, local_value in locals_dict.items()])

    @classmethod
    def from_module(cls, provider_module):
        imported = __import__(provider_module, {}, {})

        return cls.from_mixed_type_list(
            [getattr(imported, name) for name in dir(imported)])

    @classmethod
    def from_mixed_type_list(cls, mixed_type_list):
        providers = ProviderList()

        for mixed_type in mixed_type_list:
            if isinstance(mixed_type, ProviderList):
                providers += mixed_type
        return providers

    def get_provider(self, ident):
        if ident.startswith('_'):
            return lambda *args: \
                '(FAIL: identifer "{0}" begins with an underscore, args were {1})'.format(
                    ident, str(args))
        ident = ident.lower()

        for provider in self:
            if hasattr(provider, ident):
                return getattr(provider, ident)
            if isinstance(provider, dict) and ident in provider:
                return provider[ident]
        return lambda *args: \
            '(FAIL: identifier "{0}" not found, args were {1})'.format(ident, str(args))

    def get_provider_func(self, ident, *args):
        return lambda: str(self.get_provider(ident)(*args))

    def call_provider(self, ident, args):
        return self.get_provider(ident)(*args)

    def seed_providers(self, seed):
        for provider in self:
            provider.seed(seed)
