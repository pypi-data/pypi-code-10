import logging
from pyramid.i18n import TranslationStringFactory
from ringo.lib.i18n import translators
from ringo.lib.extension import register_modul
from ringo.lib.helpers import dynamic_import

# Import models so that alembic is able to autogenerate migrations
# scripts.
from ringo_tag.model import Tag

log = logging.getLogger(__name__)

modul_config = {
    "name": "tag",
    "label": "Tag",
    "label_plural": "Tags",
    "clazzpath": "ringo_tag.model.Tag",
    "str_repr": "%s|name",
    "display": "admin-menu",
    "actions": ["list", "read", "update", "create", "delete"]
}


def includeme(config):
    """Registers a new modul for ringo.

    :config: Dictionary with configuration of the new modul

    """
    modul = register_modul(config, modul_config)
    Tag._modul_id = modul.get_value("id")
    translators.append(TranslationStringFactory('ringo_tag'))
    config.add_translation_dirs('ringo_tag:locale/')
