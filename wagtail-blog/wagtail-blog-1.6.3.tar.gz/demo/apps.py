from django.apps import AppConfig
from actstream import registry
from django.apps import apps

get_model = apps.get_model


class DemoConfig(AppConfig):
    name = 'demo'

    def ready(self):
        print('!!!!!!!!!!!!!!!!!!!!')
        registry.register(get_model('auth.User'))
