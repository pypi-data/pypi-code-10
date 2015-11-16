import os
import hashlib

from django import template
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe
from django.contrib.staticfiles import finders
from django.conf import settings
from django.core.cache import cache
from django.forms import forms
from crispy_forms.exceptions import CrispyError
from django.template.loader import get_template
from django.template import Context

TEMPLATE_PACK = getattr(settings, 'CRISPY_TEMPLATE_PACK', 'bootstrap')

register = template.Library()


class MinifyJs(template.Node):

  def __init__(self, nodelist):
    files = nodelist
    self.js=[]
    m = hashlib.md5()
    m.update(' '.join(files).encode('utf-8'))
    hash = m.hexdigest()
    cached = not settings.DEBUG and cache.get(hash, False)
    
    if not cached:
      for file in files:
        if not (file[0] == file[-1] and file[0] in ('"', "'")):
          raise template.TemplateSyntaxError("minifyjs tag's arguments should be in quotes")
        file = file[1:-1]
        result = finders.find(file)
        if not result:
          raise Exception("Unable to find '{}' in:\n{}".format(file, '\n'.join("%s" % location for location in finders.searched_locations)))
        if isinstance(result, (list, tuple)):
          result = result[0]
        if settings.DEBUG:
          self.js.append('{}{}'.format(settings.STATIC_URL, file))
        else:
          path = os.path.realpath(result)
          handle = open(path, 'r')
          self.js.append(handle.read())
          handle.close()
      if not settings.DEBUG:
        handle = open(os.path.join(settings.STATIC_ROOT, '{}.js'.format(hash)), 'w+')
        handle.write(';\n'.join(self.js))
        handle.close()
        cache.set(hash, True)
    if not settings.DEBUG:
      self.js = ['{}{}.js'.format(settings.STATIC_URL, hash),]

  def render(self, context):
    return mark_safe('\n'.join('<script type="text/javascript" src="{}"></script>'.format(path) for path in self.js))


def minifyjs(parser, token):
  try:
    nodelist = token.split_contents()[1:]
  except:
    raise template.TemplateSyntaxError("%r tag requires at least one filename" % token.contents.split()[0])
  return MinifyJs(nodelist)

minifyjs = register.tag(minifyjs)


@register.filter(name='as_crispy_field_only')
def as_crispy_field(field, template_pack=TEMPLATE_PACK):
    """
    Renders a form field like a django-crispy-forms field::

        {% load crispy_forms_tags %}
        {{ form.field|as_crispy_field }}

    or::

        {{ form.field|as_crispy_field:"bootstrap" }}
    """
    if not isinstance(field, forms.BoundField) and DEBUG:
        raise CrispyError('|as_crispy_field got passed an invalid or inexistent field')

    template = get_template('%s/field.html' % template_pack)
    c = Context({'field': field, 'form_show_errors': True, 'form_show_labels': False})
    return template.render(c)
