from springpython.config import YamlConfig, XMLConfig
from springpython.context import ApplicationContext

__author__ = 'David Anderson'
__version__ = "0.1.0"

class Spring(object):
    def __init__(self, app=None):
        self.app = app

        self._context = None

        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        app.extensions = getattr(app, "extensions", {})
        app.extensions["spring"] = self

        # set any defaults
        app.config.setdefault('SPRING_YAML', None)
        app.config.setdefault('SPRING_OBJS', None)
        app.config.setdefault('SPRING_XML', None)

    @property
    def context(self):
        if self._context is None:
            config_loaders = []
            if self.app.config['SPRING_YAML']:
                [config_loaders.append(YamlConfig(config_yaml)) for config_yaml in
                 self.app.config['SPRING_YAML'].split(',')]

            if self.app.config['SPRING_XML']:
                [config_loaders.append(XMLConfig(config_xml)) for config_xml in
                 self.app.config['SPRING_XML'].split(',')]

            if self.app.config['SPRING_OBJS']:
                [config_loaders.append(conf_obj) for conf_obj in self.app.config['SPRING_OBJS']]

            self._context = ApplicationContext(config_loaders)

        return self._context