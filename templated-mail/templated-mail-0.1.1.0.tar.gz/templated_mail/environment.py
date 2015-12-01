
import os
from jinja2 import Environment
from simple_configparser import SimpleConfigParser
from .template import MessageTemplate


class MessageEnvironment(Environment):

    """
    A jinja2 Environment which overrides the `get_template`
    method to do special parsing for templates ending
    in '.msg'.

    If one of these files is found, returns the
    resulting MessageTemplate. Otherwise, a normal
    template is returned.

    """

    def __init__(self, *args, **kwargs):
        super(MessageEnvironment, self).__init__(*args, **kwargs)

    def get_template(self, name, parent=None, globals=None):

        if not name.endswith('.msg'):
            return super(MessageEnvironment, self).get_template(name, parent, globals)
        else:

            with open(os.path.join(self.loader.search_path, name)) as f:
                try:
                    parser = SimpleConfigParser()
                    parser.read_file(f)
                    return MessageTemplate(self, parser.items())
                except OSError:
                    print('couldn\'t find the file')
                    return None