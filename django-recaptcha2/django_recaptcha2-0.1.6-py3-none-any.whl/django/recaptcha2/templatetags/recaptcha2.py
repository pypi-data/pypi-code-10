from django import template
from django.conf import settings

register = template.Library()

@register.simple_tag
def recaptcha_key():
    return settings.RECAPTCHA_PUBLIC_KEY

@register.inclusion_tag('snowpenguin/recaptcha/recaptcha_init.html')
def recaptcha_init():
    return {'explicit': False}

@register.inclusion_tag('snowpenguin/recaptcha/recaptcha_init.html')
def recaptcha_explicit_init():
    return {'explicit': True}

@register.inclusion_tag('snowpenguin/recaptcha/recaptcha_explicit_support.html')
def recaptcha_explicit_support():
    return {}