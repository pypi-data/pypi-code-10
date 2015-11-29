class Container():

    def __init__(self):
        self.__container = {}

    def register(self, key, instance):
        self.__container[key] = instance;

    def get(self, key):
        obj = self.__container[key]

        if (hasattr(obj, '__call__')):
            obj = obj(self)

        return obj 