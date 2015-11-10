# coding: utf-8
import re
import six

from sqlalchemy.types import TypeDecorator, UnicodeText

from pyuploadcare.api_resources import File, FileGroup, RE_EFFECTS
from pyuploadcare.exceptions import InvalidRequestError

__ALL__ = ('FileType', 'ImageType', 'FileGroupType')

COMPILED_EFFECTS_RE = re.compile('^{0}$'.format(RE_EFFECTS))


class FileType(TypeDecorator):
    """ Field type which stores File as Uploadcare CDN url.
    """
    impl = UnicodeText

    def process_bind_param(self, value, dialect):
        if not value:
            return value

        if isinstance(value, File):
            return value.cdn_url

        if isinstance(value, six.string_types):
            ufile = self.build_object(value)

            if not ufile.is_stored():
                ufile.store()

            return ufile.cdn_url

        raise ValueError('Invalid type of value: {}'.format(type(value)))

    def process_result_value(self, value, dialect):
        if not value:
            return value

        return self.build_object(value)

    def copy(self):
        return type(self)()

    def build_object(self, value):
        return File(value)


class FileGroupType(FileType):
    """ Field type which stores FileGroup as Uploadcare CDN url.
    """
    def build_object(self, value):
        return FileGroup(value)


class ImageType(FileType):
    """ Variants of `FileType` which works with images.

    It supports default effects e.g. you can define effects according by
    documentation: https://uploadcare.com/documentation/cdn/#image-operations
    which will be applied to received images:

        Column('file', ImageType(effects='-/resize/200x300'))
        Column('file', ImageType(effects='-/resize/200x300/-/autorotate/yes/'))

    """

    def __init__(self, effects=None, *args, **kwargs):
        if effects and not isinstance(effects, six.string_types):
            raise ValueError('Value of effects must be a string type, '
                             'not {0}'.format(type(effects)))

        if effects and not COMPILED_EFFECTS_RE.match(effects):
            raise ValueError('Invalid value for effects param: '
                             '{0}'.format(effects))
        self.effects = effects
        super(ImageType, self).__init__(*args, **kwargs)

    def build_object(self, value):
        ufile = super(ImageType, self).build_object(value)
        ufile.default_effects = (self.effects or '').lstrip('-/')

        if not ufile.is_image():
            raise ValueError('This is not image')

        return ufile

    def copy(self):
        return ImageType(effects=self.effects)
