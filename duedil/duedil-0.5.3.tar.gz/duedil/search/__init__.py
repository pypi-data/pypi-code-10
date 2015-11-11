
from importlib import import_module

class SearchResource(object):
    attribute_names = None
    locale = 'uk'
    rid = None
    path = None
    result_obj = {}

    def __init__(self, client, id=None, locale='uk', load=False, **kwargs):
        if not self.attribute_names:
            raise NotImplementedError(
                "Resources must include a list of allowed attributes")

        self.rid = id
        assert(locale in ['uk', 'roi'])
        self.locale = locale
        self.client = client
        self.should_load = True if load else False
        if load:
            self.load()

        if kwargs:
            self._set_attributes(**kwargs)

    def _set_attributes(self, missing=False, **kwargs):
        for k, v in kwargs.items():
            if k in self.attribute_names:
                self.__setattr__(k, v)

        if missing is True:
            for allowed in self.attribute_names:
                if allowed not in kwargs:
                    self.__setattr__(allowed, None)

    def load(self):
        result = self.client.get(self.endpoint)
        self._set_attributes(**result)

    def __getattr__(self, name):
        """
        lazily return attributes, only contact duedil if necessary
        """
        try:
            return super(SearchResource, self).__getattribute__(name)
        except AttributeError:
            if name in self.attribute_names:
                self.load()
                return super(SearchResource, self).__getattribute__(name)
            elif name in self.result_obj.keys():
                # Assumes subclass has dict defined called result_obj, this maps attribute name to
                # string of module path including class to be instaniated.
                # The below dynamically imports the module and then gets the class, then returns and instance of the class
                mod_path, klass_str = self.result_obj[name].rsplit('.', 1)
                mod = import_module(mod_path)
                klass = getattr(mod, klass_str)
                return klass(self.rid, client=self.client, locale=self.locale, load=self.should_load)
            else:
                raise

    def __eq__(self, other):
        if hasattr(other, 'rid'):
            return self.rid == other.rid
        return self.rid == other
