"""Providers used in the binding process."""

# pylint: disable-msg=C0111
#         providers are so small that we can safely omit doc comments

from snakeguice.decorators import inject
from snakeguice.interfaces import Injector


def create_simple_provider(cls):
    class DynamicSimpleProvider(object):

        @inject(injector=Injector)
        def __init__(self, injector):
            self._injector = injector

        def get(self):
            return self._injector.create_object(cls)

    return DynamicSimpleProvider


class __InstanceProvider(object):
    __slots__ = ['__instance']

    def __init__(self, instance):
        self.__instance = instance

    def get(self):
        return self.__instance


def create_instance_provider(instance):
    return __InstanceProvider(instance)
