from coreinit.utils.exceptions import *
from coreinit.utils.installer import *
from coreinit import settings

def configure():
    try:
        import jinja2
    except:
        install_pip(['jinja2'])


def render(template, context):
    from jinja2 import Environment, FileSystemLoader

    if settings.TEMPLATE_PATH is None:
        raise ConfigurationException('TEMPLATE_PATH not configured')

    env = Environment(loader=FileSystemLoader(settings.TEMPLATE_PATH))
    template = env.get_template(template)

    return template.render(**context)
