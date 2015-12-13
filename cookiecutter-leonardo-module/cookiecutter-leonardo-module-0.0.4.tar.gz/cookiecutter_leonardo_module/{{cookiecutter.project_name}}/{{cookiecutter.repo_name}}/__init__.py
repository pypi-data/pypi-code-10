
from django.apps import AppConfig

from .widget import *

default_app_config = '{{ cookiecutter.repo_name }}.Config'


LEONARDO_APPS = ['{{ cookiecutter.repo_name }}']


class Config(AppConfig):
    name = '{{ cookiecutter.repo_name }}'
    verbose_name = "{{ cookiecutter.project_name }}"
