import base64
import binascii

from django.http import HttpResponse

from .models import StaticContent


class StaticContentMiddleware(object):
    def process_response(self, request, response):

        # Only check on pages that do not exist. Do not override CMS pages
        if response.status_code != 404:
            return response

        # Get the full request path
        path = request.get_full_path()

        # Try to get a static content object at the current path
        try:
            # Get object
            content_object = StaticContent.objects.get(url=path)

            if content_object.base64:
                content_object.content = base64.decodestring(content_object.content)

            # Return our content object
            return HttpResponse(content_object.content, content_type=content_object.content_type)

        except StaticContent.DoesNotExist:

            # Return the default response at this point
            return response
