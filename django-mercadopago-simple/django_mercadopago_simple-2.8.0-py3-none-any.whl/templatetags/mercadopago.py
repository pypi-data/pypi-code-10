from django import template

register = template.Library()


@register.inclusion_tag('django_mercadopago/payment_button.html')
def payment_button(preference):
    return {'preference': preference}


# TODO: Another tag for css/js?
