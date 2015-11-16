from django.db import models
from django.conf import settings


class AutoTextileModel(models.Model):

  _textile = ()

  class Meta:
    abstract = True

  def save(self, *args, **kwargs):
    from textile import textile
    suffixes = ['']
    suffixes.extend(['_{}'.format(x) for (x,y) in settings.LANGUAGES])
    for field in self._textile:
      for s in suffixes:
        try:
          orig = getattr(self, '{}{}'.format(field, s))
        except Exception:
          continue
        if orig is not None:
          compiled_field_name = 'compiled_{}{}'.format(field, s)
          if not hasattr(self, compiled_field_name):
            raise Exception('Coul not find `{}` in model `{}`'.format(compiled_field_name, self.__class__))
          setattr(self, compiled_field_name, textile(orig))
    return super(AutoTextileModel, self).save(*args, **kwargs)

