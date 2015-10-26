import json

from django.core.urlresolvers import reverse
from django.test import TestCase, RequestFactory
from restify.authentication import ApiKeyAuthentication


class RestApiTestCase(TestCase):
    RESOURCE = None

    def _set_auth_data(self, request, **kwargs):
        if isinstance(self.RESOURCE.authentication, ApiKeyAuthentication):
            request.GET['username'] = kwargs['user'].username
            request.GET['api_key'] = kwargs['user'].api_key.key

    def _get_response(self, method_name, data, user, **extra):
        rfactory = RequestFactory()

        try:
            resource_url = reverse('api:{0}'.format(self.RESOURCE._meta.resource_name))
        except AttributeError: #AttributeError: 'Settings' object has no attribute 'ROOT_URLCONF'
            resource_url = '/'

        method = getattr(rfactory, method_name)
        request = method(resource_url, data, **extra)
        request.session = {}
        setattr(request, method_name.upper(), data)

        if user:
            self._set_auth_data(request, user=user)

        resource = self.RESOURCE()
        resource.request = request
        resp = resource(request, **extra)

        if resp['Content-Type'] == 'application/json':
            resp.json = json.loads(resp.content.decode('utf8'))

        return resp

    def post(self, data, user=None, **extra):
        return self._get_response('post', data, user, **extra)

    def get(self, query={}, user=None, **extra):
        return self._get_response('get', data=query, user=user, **extra)
