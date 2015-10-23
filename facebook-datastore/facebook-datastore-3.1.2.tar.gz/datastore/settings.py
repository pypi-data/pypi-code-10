TIME_ZONE = 'Europe/Warsaw'
LANGUAGE_CODE = 'pl'
SITE_ID = 1
USE_I18N = True
USE_L10N = True
USE_TZ = True
MEDIA_URL = '/media/'
STATIC_URL = '/static/'

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

SECRET_KEY = '92+lsozvq7&amp;kfl5%j1o91!5cqo5f5r@d062g&amp;bzwg2&amp;v^%s9!v'

TEMPLATE_LOADERS = (
    'django.template.loaders.app_directories.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.views.decorators.csrf._EnsureCsrfCookie',
)

ROOT_URLCONF = 'datastore.urls'

WSGI_APPLICATION = 'datastore.wsgi.application'

PROJECT_APPS = (
    'facebook_datastore',
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.gis',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'facebook_auth',
    'facebook_javascript_authentication',
    'facebook_javascript_sdk',
    'south',
)
INSTALLED_APPS += PROJECT_APPS

AUTHENTICATION_BACKENDS= (
    'django.contrib.auth.backends.ModelBackend',
    'facebook_auth.backends.FacebookJavascriptBackend',
)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}
