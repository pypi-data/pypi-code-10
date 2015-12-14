"""Base settings shared by all environments.
This is a reusable basic settings file.
"""
from configurations import Configuration
import os
from . import mixins


class StandardConfiguration(mixins.UnifiedDebugMixin,
                        mixins.SecretSettingsMixin,
                        mixins.AllowedHostsMixin,
                        mixins.LoggingMixin,
                        mixins.DatabaseMixin,
                        mixins.StaticMediaMixin,
                        mixins.EmailMixin,
                        mixins.BaseUrlMixin,
                        Configuration):
    """A configuration that collects together lots of standard
    configuration patterns for use across projects."""

    TIME_ZONE = 'GB'
    USE_TZ = True
    USE_I18N = True
    USE_L10N = True
    LANGUAGE_CODE = 'en-GB'
    LANGUAGES = (
        ('en-GB', 'British English'),
    )

    SITE_ID = 1
    LOGIN_URL = '/login/'
    LOGOUT_URL = '/logout/'
    LOGIN_REDIRECT_URL = '/'

    STATIC_URL = '/static/'
    MEDIA_URL = '/uploads/'

    @property
    def TEMPLATES(self):
        return [
            {
                'BACKEND': 'django.template.backends.django.DjangoTemplates',
                'DIRS': [os.path.join(self.PROJECT_ROOT, 'templates')],
                'APP_DIRS': True,
                'OPTIONS': {
                    'context_processors': [
                        'django.contrib.auth.context_processors.auth',
                        'django.template.context_processors.debug',
                        'django.template.context_processors.i18n',
                        'django.template.context_processors.media',
                        'django.template.context_processors.static',
                        'django.template.context_processors.tz',
                        'django.core.context_processors.request',
                        'django.contrib.messages.context_processors.messages',
                    ],
                },
            },
        ]

    ROOT_URLCONF = 'urls'

    @property
    def INSTALLED_APPS(self):
        return [
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.sessions',
            'django.contrib.sites',
            'django.contrib.messages',
            'django.contrib.staticfiles',
            'django.contrib.admin',
        ]

    @property
    def MIDDLEWARE_CLASSES(self):
        return [
            'django.contrib.sessions.middleware.SessionMiddleware',
            'django.middleware.common.CommonMiddleware',
            'django.middleware.csrf.CsrfViewMiddleware',
            'django.contrib.auth.middleware.AuthenticationMiddleware',
            'django.contrib.messages.middleware.MessageMiddleware',
            'django.middleware.clickjacking.XFrameOptionsMiddleware',
        ]

    PROTOCOL = 'http'

    MANAGERS = ADMINS = (
        ('David Seddon', 'david@seddonym.me'),
    )
