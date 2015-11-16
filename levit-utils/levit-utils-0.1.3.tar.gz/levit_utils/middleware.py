
from django.http import HttpResponseRedirect
from django.utils import translation

class LocaleMiddleware(object):

  def process_request(self, request):
    language = translation.get_language_from_request(request)
    try:
      l2 = request.session.get('language', None)
    except AttributeError:
      l2 = None
    if l2 is None and language == 'fr' and request.path[:3] != '/fr' and request.path[:6] != '/admin':
      return HttpResponseRedirect('/fr{}'.format(request.path))

  def process_response(self, request, response):
    language = translation.get_language()
    if 'Content-Language' not in response:
      response['Content-Language'] = language
    if request.session.get('language', None) != language:
      request.session['language'] = language
      request.session.save()
    return response
