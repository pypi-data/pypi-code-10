
from django.apps import AppConfig


default_app_config = 'leonardo_module_pagepermissions.PagePermissonsConfig'


class Default(object):

    apps = [
        'pagepermissions',
        'leonardo_module_pagepermissions',
    ]

    page_extensions = [
        'pagepermissions.extension',
    ]


class PagePermissonsConfig(AppConfig, Default):
    name = 'leonardo_module_pagepermissions'
    verbose_name = ("Page Permissions")


default = Default()
