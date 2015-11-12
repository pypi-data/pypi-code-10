# coding: utf-8
import six
from wtforms import Field
from wtforms.widgets import HiddenInput

from pyuploadcare import conf
from pyuploadcare.api_resources import File, FileGroup
from pyuploadcare.exceptions import InvalidParamError

__ALL__ = ('FileWidget', 'FileField', 'ImageField', 'FileGroupField')


class FileWidget(HiddenInput):
    """ Widget which sets up Uploadcare Widget.

    It adds hidden input with basic Widget's params, e.g `data-public-key`
    """
    def __call__(self, field, **kwargs):
        default_params = {
            'role': 'uploadcare-uploader',
            'data-public-key': conf.pub_key,
        }

        if conf.upload_base:
            default_params['data-upload-base-url'] = conf.upload_base

        default_params.update(kwargs)
        return super(FileWidget, self).__call__(field, **default_params)


class FileField(Field):
    """ Field which uses ``FileWidget`` and returns ``File`` object.
    """
    widget = FileWidget()
    object_type = File

    def _value(self):
        if isinstance(self.data, self.object_type):
            return self.data.cdn_url
        return self.data or ''

    def pre_validate(self, form):
        if not self.raw_data:
            return

        value = self.raw_data[0]

        if not isinstance(value, six.string_types):
            raise ValueError('Value must be type of string')

    def process_formdata(self, valuelist):
        if valuelist and valuelist[0]:
            self.data = self.object_type(valuelist[0])
        else:
            self.data = None


class FileGroupField(FileField):
    """ Field which uses ``FileWidget`` and returns ``FileGroup`` object.
    """
    object_type = FileGroup

    def __call__(self, **kwargs):
        kwargs['data-multiple'] = ''
        return super(FileGroupField, self).__call__(**kwargs)


class ImageField(FileField):
    def __init__(self, *args, **kwargs):
        self.manual_crop = kwargs.pop('manual_crop', None)
        super(ImageField, self).__init__(*args, **kwargs)

    def __call__(self, **kwargs):
        kwargs['data-images-only'] = ''
        if self.manual_crop:
            kwargs['data-crop'] = self.manual_crop
        return super(ImageField, self).__call__(**kwargs)
