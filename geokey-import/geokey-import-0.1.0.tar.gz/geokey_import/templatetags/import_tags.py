from django import template
from django.template.loader import render_to_string


register = template.Library()


@register.simple_tag
def display_field(field):
    value = field.split(':', 1)[1]

    if value == 'None':
        return '-'
    else:
        return value


@register.simple_tag
def field_html(field, properties):
    if field.fieldtype == 'DateField':
        classes = 'date'
        add_on = 'data-date-format="YYYY-MM-DD"'
    elif field.fieldtype == 'DateTimeField':
        classes = 'datetime'
        add_on = 'data-date-format="YYYY-MM-DD H:mm"'
    elif field.fieldtype == 'TimeField':
        classes = 'time'
        add_on = 'data-date-format="H:mm"'
    else:
        classes = ''
        add_on = ''

    return render_to_string(
        'categories/field_form.html',
        {
            'field': field,
            'field_type': get_field_type(field.fieldtype),
            'value': get_field_value(properties, field.key),
            'classes': classes,
            'add_on': add_on
        }
    )


def get_field_type(field_type):
    if field_type == 'NumericField':
        return 'number'

    return 'text'


@register.filter
def get_field_value(properties, key):
    value = properties.get(key)
    if value is None:
        value = ''

    return value
