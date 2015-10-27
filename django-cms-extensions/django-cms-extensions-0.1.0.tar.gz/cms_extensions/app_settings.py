from django.conf import settings as __settings

AUTO_EXPORT = getattr(__settings, 'CMS_AUTO_EXPORT', False)
EXPORT_ROOT = getattr(__settings, 'CMS_EXPORT_ROOT', 'export')
DEFAULT_LANGUAGE = __settings.CMS_LANGUAGES[1][0]['code']
