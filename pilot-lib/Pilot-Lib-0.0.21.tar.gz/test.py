
d = {
    "ENABLE": True,
    "FACEBOOK": {
        "ENABLE": True,
        "CLIENT_ID": "FB-1"
    },
    "GOOGLE": {
        "ENABLE": False,
        "CLIENT_ID": "G+"
    }
}

credentials = {}
for name, prop in d.items():
    if isinstance(prop, dict):
        if prop["ENABLE"]:
            _name = name.lower()
            credentials[_name] = prop["CLIENT_ID"]
print credentials
exit()

__author__ = 'mardochee.macxis'

class classproperty(property):
    """
    Just like @property, @classproperty let you do the same on class level
    """
    def __get__(self, cls, owner):
        return classmethod(self.fget).__get__(None, owner)()

class PilotViewDecoratorsMixin(object):
    @classproperty
    def decorators(cls):
        return "Boom"


class UserMixin(PilotViewDecoratorsMixin):
    _decorators = ["C", "D"]
    pass

class AdminMixin(PilotViewDecoratorsMixin):
    _decorators = ["A", "B"]
    pass


class View(UserMixin, AdminMixin):
    pass


print View.decorators

class MetaDataMixin(object):

    __meta__ = {
        "page": {
            "title": "",
            "description": "",
            "keywords": ""
        },
        "opengraph": {},
        "twitter": {},
        "googleplus": {}
    }

    @classmethod
    def __get_meta(cls, key):
        return Pilot._global_context.get("__meta__", {})

    @classmethod
    def __meta_page(cls, **kwargs):
        if "title" in kwargs:
            title = kwargs["title"]
            if "title"

    if append or prepend:
        _page_title =
        if append:
            title = "%s %s" % (_page_title, title)
        else:
            title = "%s %s" % (title, _page_title)


    @classmethod
    def __meta_opengraph(cls, **kwargs):
        pass

    @classmethod
    def __meta_twitter(cls, **kwargs):
        pass

    @classmethod
    def __meta_googleplus(cls, **kwargs):
        pass


    @classmethod
    def get_(cls, k):
        pass
