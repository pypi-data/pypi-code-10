__author__ = 'cltanuki'
from django.forms import MultiValueField, ChoiceField, CharField, MultiWidget, TextInput, Select


class PhoneWidget(MultiWidget):
    def __init__(self, code_length, num_length, attrs=None):
        widgets = [TextInput(attrs={'size': code_length, 'maxlength': code_length, 'min-width': '40px!'}),
                   TextInput(attrs={'size': num_length, 'maxlength': num_length, 'min-width': '160px!'})]
        super(PhoneWidget, self).__init__(widgets, attrs)

    def decompress(self, value):
        if value:
            return [value.code, value.number]
        else:
            return ['', '']

    def format_output(self, rendered_widgets):
        return '+7' + '(' + rendered_widgets[0] + ') - ' + rendered_widgets[1]


class PhoneField(MultiValueField):
    def __init__(self, code_length, num_length, *args, **kwargs):
        list_fields = [CharField(max_length=code_length),
                       CharField(max_length=num_length)]
        super(PhoneField, self).__init__(list_fields, widget=PhoneWidget(code_length, num_length), *args, **kwargs)

    def compress(self, values):
        return '+7' + values[0] + values[1]


class TimeWidget(MultiWidget):
    def __init__(self, h_choices, m_choices, attrs=None):
        widgets = [Select(choices=h_choices),
                   Select(choices=m_choices)]
        super(TimeWidget, self).__init__(widgets, attrs)

    def decompress(self, value):
        if value:
            return [value.hours, value.minutes]
        else:
            return ['', '']


class TimeField(MultiValueField):
    def __init__(self, h_choices, m_choices, *args, **kwargs):
        list_fields = [ChoiceField(choices=h_choices),
                       ChoiceField(choices=m_choices)]
        super(TimeField, self).__init__(list_fields, widget=TimeWidget(h_choices, m_choices), *args, **kwargs)

    def compress(self, values):
        return values[0] + ':' + values[1]