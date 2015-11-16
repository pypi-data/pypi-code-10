from django.conf import settings


def environ_settings(request):

  rv = {}

  for item in ['SITE_URL',]:

    try:
      rv[item] = getattr(settings,item)
    except Exception:
      rv[item] = ''

  return rv
