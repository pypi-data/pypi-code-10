from django import forms
from django.forms.widgets import HiddenInput
import re

class ChoiceWithOtherWidget(forms.MultiWidget):
  def __init__(self,choices=[(-1, 'other'),], attrs=None):
    self.choices = choices
    widgets = (
      forms.Select(choices=choices),
      forms.TextInput()
    )
    super(ChoiceWithOtherWidget, self).__init__(widgets, attrs)

  def decompress(self, value):
    if value:
      if value in [x[0] for x in self.choices]:
        return [value, '']
      else:
        return [self.choices[-1][0], value]
    return [None, None]

  def format_output(self, rendered_widgets):
    return "<div class='choice_with_other'>{}{}</div>".format(rendered_widgets[0], rendered_widgets[1])


class ChoiceWithOtherField(forms.MultiValueField):

  def __init__(self, *args, **kwargs):
    fields = [
        forms.ChoiceField(widget=forms.Select(), *args, **kwargs),
        forms.CharField(required=False)
    ]
    self.choices = kwargs.pop('choices')
    self._was_required = kwargs.pop('required', True)
    kwargs['required'] = False
    widget = ChoiceWithOtherWidget(choices=self.choices)
    super(ChoiceWithOtherField, self).__init__(widget=widget, fields=fields, *args, **kwargs)

  def compress(self, value):
    if self._was_required and not value or value[0] in (None, ''):
      raise forms.ValidationError(self.error_messages['required'])
    if not value:
      return ''
    if value[0] == self.fields[0].choices[-1][0]:
      return value[1]
    return value[0]

  def deconstruct(self):
    name, path, args, kwargs = super(VatField, self).deconstruct()
    kwargs['choices']=[]
    return name, path, args, kwargs


EMPTY_VALUES = (None, '')

VAT_CHOICES = (
('','----------'),
('AT','AT-Austria'),
('BE','BE-Belgium'),
('BG','BG-Bulgaria'),
('CY','CY-Cyprus'),
('CZ','CZ-Czech Republic'),
('DE','DE-Germany'),
('DK','DK-Denmark'),
('EE','EE-Estonia'),
('EL','EL-Greece'),
('ES','ES-Spain'),
('FI','FI-Finland'),
('FR','FR-France '),
('GB','GB-United Kingdom'),
('HU','HU-Hungary'),
('IE','IE-Ireland'),
('IT','IT-Italy'),
('LT','LT-Lithuania'),
('LU','LU-Luxembourg'),
('LV','LV-Latvia'),
('MT','MT-Malta'),
('NL','NL-The Netherlands'),
('PL','PL-Poland'),
('PT','PT-Portugal'),
('RO','RO-Romania'),
('SE','SE-Sweden'),
('SI','SI-Slovenia'),
('SK','SK-Slovakia'),
)

class VatWidget(forms.MultiWidget):
  """docstring for VatWidget"""
  def __init__(self,choices=VAT_CHOICES, attrs=None):
    widgets = (
      forms.Select(choices=choices),
      forms.TextInput()
      )
    super(VatWidget, self).__init__(widgets, attrs)

  def value_from_datadict(self, data, files, name):
    value = [widget.value_from_datadict(data, files, name + '_%s' % i) for i, widget in enumerate(self.widgets)]
    try:
      country, code = value
      #the spaces and the dots are removed
      code=code.replace(".","").replace(" ","")
    except:
      return data.get(name, None)
    if code not in EMPTY_VALUES:
      if country in EMPTY_VALUES:
        try:
          # ex. code="FR09443710785", country="".
          empty, country, code = re.split('([a-zA-Z]+)',code )
        except:
          return ['', code]
      else:
        #ex. code ="FR09443710785", country="FR".
        re_code = re.compile(r'^%s(\d+)$' % country)
        if re_code.match(code):
          code = code.replace(country,"",1)
      try: country = country.upper()
      except:pass
    return [country, code]

  def format_output(self, rendered_widgets):
    return "%s&nbsp;%s" % (rendered_widgets[0], rendered_widgets[1])

  def decompress(self, value):
    if value:
      try:country, code = value
      except:
        country = None
        code = value
      if country in EMPTY_VALUES:
        try:empty, country, code = re.split('([a-zA-Z]+)', code)
        except:pass
      return [country, code]
    return [None, None]

class VatHiddenWidget(VatWidget):
  """
  A Widget that splits vat input into two <input type="hidden"> inputs.
  """
  def __init__(self, attrs=None):
    widgets = (HiddenInput(attrs=attrs), HiddenInput(attrs=attrs))
    super(VatWidget, self).__init__(widgets, attrs)

class VatField(forms.MultiValueField):
  """docstring for VatField"""
  hidden_widget = VatHiddenWidget
  def __init__(self, choices=VAT_CHOICES, *args, **kwargs):
    # Set 'required' to False on the individual fields, because the
    # required validation will be handled by MultiValueField, not by those
    # individual fields.
    fields = (
      forms.ChoiceField(required=True, choices=choices),
      forms.CharField(required=True),
    )
    for f in fields:
      f.required = False
    widget = VatWidget(choices=choices)
    super(VatField, self).__init__(widget=widget, fields=fields, *args, **kwargs)

  def compress(self, data_list):
    if data_list:
      return "".join(data_list)
    return None

  def deconstruct(self):
    name, path, args, kwargs = super(VatField, self).deconstruct()
    kwargs['choices']=VAT_CHOICES
    return name, path, args, kwargs