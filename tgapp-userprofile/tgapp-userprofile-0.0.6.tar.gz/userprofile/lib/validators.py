# -*- coding: utf-8 -*-
import tg
from formencode import FancyValidator
from tgext.pluggable import app_model
from userprofile.model import DBSession

try:
    from tgext.datahelpers.validators import SQLAEntityConverter as _SQLAEntityConverter
except ImportError:
    class _SQLAEntityConverter(object):
        def __init__(self, *args, **kwargs): pass

try:
    from tgext.datahelpers.validators import MingEntityConverter as _MingEntityConverter
except ImportError:
    class _MingEntityConverter(object):
        def __init__(self, *args, **kwargs): pass


def _get_storage_backend():
    tg_conf = tg.config
    if tg_conf.get('use_sqlalchemy', False):
        return 'sqlalchemy'
    elif tg_conf.get('use_ming', False):
        return 'ming'
    else:
        raise ValueError('Turbopress should be used with sqlalchemy or ming')


class ModelEntityConverter(FancyValidator):
    def __init__(self, klass, slugified=False):
        super(FancyValidator, self).__init__(not_empty=True)
        self.model_name = klass
        self.slugified = slugified
        self._converters = {}

    def _create_converter(self, backend):
        if backend == 'sqlalchemy':
            return _SQLAEntityConverter(getattr(app_model, self.model_name),
                                        session=DBSession,
                                        slugified=self.slugified)
        elif backend == 'ming':
            return _MingEntityConverter(getattr(app_model, self.model_name),
                                        slugified=self.slugified)

    @property
    def _converter(self):
        storage_backend = _get_storage_backend()
        try:
            converter = self._converters[storage_backend]
        except KeyError:
            self._converters[storage_backend] = converter = self._create_converter(storage_backend)
        return converter

    def _convert_to_python(self, value, state):
        return self._converter._to_python(value, state)

    def _convert_from_python(self, value, state):
        return self._converter._from_python(value, state)

    def _validate_python(self, value, state):
        return self._converter.validate_python(value, state)

    _to_python = _convert_to_python
    _from_python = _convert_from_python
    validate_python = _validate_python