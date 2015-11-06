# -*- coding: utf-8 -*-
from zope.interface import Interface, implementer
import requests
import json


class IDocumentEngine(Interface):
    def create_documents(self, data, system_token):
        '''create the documents with incoming data'''

    def get_pdf_document(self, generation_id, system_token, accept='application/pdf'):
        '''get the document. Accept is either application/pdf (default) or either text/html'''

@implementer(IDocumentEngine)
class DocumentEngine(object):
    def __init__(self, baseurl, template_id):
        self.baseurl = baseurl
        self.template_id = template_id

    def _create_generation(self, system_token):
        '''create generation id'''
        data = {
            'template_id': self.template_id,
            'template_version': '1'
        }
        headers = {}
        if system_token:
            headers = {'OpenAmSSOID': system_token,
                       'Accept': 'application/json'}
        res = requests.post('{0}/generations'.format(self.baseurl), json=data, headers=headers)
        res.raise_for_status()
        return json.loads(res.text)['id']


    def _update_content(self, generation_id, data, system_token):
        '''update the content of the document'''
        headers = {}
        if system_token:
            headers = {'OpenAmSSOID': system_token,
                       'Accept': 'application/json'}
        res = requests.put('{0}/generations/{1}'.format(self.baseurl, generation_id), json=data, headers=headers)
        res.raise_for_status()

    def _create_documents(self, generation_id, system_token):
        '''create the documents'''
        headers = {}
        if system_token:
            headers = {'OpenAmSSOID': system_token}
        res = requests.post('{0}/generations/{1}/documents'.format(self.baseurl, generation_id), headers=headers)
        res.raise_for_status()
        return res

    def create_documents(self, data, system_token):
        '''create the documents with incoming data'''

        '''create generation'''
        generation_id = self._create_generation(system_token)
        '''update the content of the document'''
        self._update_content(generation_id, data, system_token)
        '''create the documents'''
        self._create_documents(generation_id, system_token)
        return generation_id

    def get_pdf_document(self, generation_id, system_token, accept='application/pdf'):
        '''get the document. Accept is either application/pdf (default) or either text/html'''
        headers = {}
        if system_token:
            headers = {'OpenAmSSOID': system_token,
                       'Accept': accept
                       }
        res = requests.get('{0}/generations/{1}/document'.format(self.baseurl, generation_id), headers=headers)
        res.raise_for_status()
        return res