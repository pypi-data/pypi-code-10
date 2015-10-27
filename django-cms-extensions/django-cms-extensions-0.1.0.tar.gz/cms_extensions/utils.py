from django.test import RequestFactory
from django.contrib.auth.models import AnonymousUser
from django.contrib.sessions.middleware import SessionMiddleware
from django.template import RequestContext
from django.template.response import TemplateResponse
from cms.utils import get_template_from_request
from . import app_settings
import os


class CMSRequestFactory(RequestFactory):
    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
        self.session_middleware = SessionMiddleware()
        self.user = AnonymousUser()

    def request(self, **request):
        # generate request
        request_obj = super(self.__class__, self).request(**request)

        # add user to request
        request_obj.user = self.user

        # add session to request
        self.session_middleware.process_request(request_obj)
        request_obj.session.save()

        return request_obj


def page_to_html(page, language=None, encoding='utf-8'):
    # generate request
    request = CMSRequestFactory().request()
    request.current_page = page

    # generate request context
    context = RequestContext(request)
    context['lang'] = language or app_settings.DEFAULT_LANGUAGE
    context['current_page'] = page

    # generate template response
    template_name = get_template_from_request(request, page)
    response = TemplateResponse(request, template_name, context)
    response.render()

    # generate html
    html = response.content.decode(encoding)

    return html


def page_to_file_name(page, export_root=app_settings.EXPORT_ROOT,
                      language=None):

    url = '%s/%s' % (language, page.get_path(language=language))

    return os.path.join(export_root, page.site.name, url, 'index.html')


def export_page(page, export_root=app_settings.EXPORT_ROOT,
                language=None):

    file_name = page_to_file_name(page, export_root, language)
    file_path = os.path.dirname(file_name)

    if not os.path.exists(file_path):
        os.makedirs(file_path)

    with open(file_name, 'w+') as file:
        file.write(page_to_html(page, language))


def delete_exported_page(page, export_root=app_settings.EXPORT_ROOT,
                         language=None):

    file_name = page_to_file_name(page, export_root, language)

    if os.path.exists(file_name):
        os.remove(file_name)

    delete_orphaned_directorys(os.path.join(app_settings.EXPORT_ROOT,
                                            page.site.name))


def delete_orphaned_directorys(root):
    for root, directories, files in os.walk(root):

        for directory in directories:
            directory = os.path.join(root, directory)

            if not os.listdir(directory):
                os.rmdir(directory)
