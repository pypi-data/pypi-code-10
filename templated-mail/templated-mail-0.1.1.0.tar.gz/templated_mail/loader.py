from contextlib import contextmanager
from jinja2.loaders import DictLoader, ChoiceLoader, FileSystemLoader

class DynamicLoader(ChoiceLoader):

    """
    A subclass of ChoiceLoader that takes a
    directory where templates can be found,
    as well as providing a contextmanager
    for adding a dict of extra string
    templates.

    """

    def __init__(self, search_path):
        self.search_path = search_path
        super(DynamicLoader, self).__init__([
            FileSystemLoader(search_path),
            DictLoader({}),
        ])

    @property
    def extra(self):
        return self.loaders[1].mapping

    @extra.setter
    def extra(self, extra):
        self.loaders[1].mapping = extra

    @contextmanager
    def add_templates(self, templates):
        try:
            self.extra = templates
            yield self
        finally:
            self.extra = {}
