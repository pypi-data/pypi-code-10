#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
.. module:: TODO
   :platform: Unix
   :synopsis: TODO.

.. moduleauthor:: Aljosha Friemann <aljosha.friemann@gmail.com>

"""

import requests, logging

class Exhibitor:
    company = contact = contact_name = contact_tel = contact_mail = subdomain = None

    def __init__(self, company, contact, contact_name, contact_tel, contact_mail, subdomain):
        self.company = company
        self.contact = contact
        self.contact_name = contact_name
        self.contact_tel = contact_tel
        self.contact_mail = contact_mail
        self.subdomain = subdomain

    @staticmethod
    def keys():
        return ['company', 'contact', 'contact_name', 'contact_tel', 'contact_mail', 'subdomain']

class Domain:
    def __init__(self, root):
        self.log = logging.getLogger(self.__class__.__name__)
        self.root = root

    def get(self, page):
        self.log.debug('requesting %s', page)
        response = requests.get(self.root + page)

        if response.status_code == requests.codes.ok:
            return response.text
        else:
            raise Exception('status code was %s' % response.status_code)

    def xpath_string(self, root, path, index = 0, fallback = ''):
        try:
            if index >= 0:
                return root.xpath(path)[index]
            else:
                return '\n'.join(root.xpath(path))
        except:
            return fallback

    def get_exhibitors(self, **kwargs):
        raise NotImplementedError

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 fenc=utf-8
