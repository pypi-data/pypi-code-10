# coding=utf-8
from Products.Five import BrowserView
from zope.component import getMultiAdapter


class JsonConfiguration(BrowserView):

    def original_call(self):
        ''' This mimic the original call
        '''
        view = getMultiAdapter(
            (self.context, self.request),
            name='tinymce-jsonconfiguration'
        )
        return view.jsonConfiguration(self.request.get('field'))

    def __call__(self):
        ''' A workaround for:
         - https://github.com/plone/Products.TinyMCE/issues/125

        Get the original configuration but declare the correct content-type
        '''
        self.request.RESPONSE.setHeader(
            'Content-type',
            'text/plain'
        )
        return self.original_call()
