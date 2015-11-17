#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
.. module:: TODO
   :platform: Unix
   :synopsis: TODO.

.. moduleauthor:: Aljosha Friemann aljosha.friemann@gmail.com

"""

import re

from lxml import html

from scrapy.model import Domain, Exhibitor

class Intec(Domain):
    def __init__(self, root, event):
        root = 'http://www.messe-intec.de' if root is None else root

        super(Intec, self).__init__(root)

        self.event = 'intec' if event is None else event
        self.request_base = "/aussteller-produkte/aussteller/ansprechpartner?event=%s" % self.event

    def get_exhibitors(self, start = 0):
        page = start
        next_button = None

        while next_button is None or next_button != []:
            attempt = 0
            url = self.request_base + "&page=%s" % page

            while attempt < 3:
                self.log.info('requesting page %s (%s. attempt)', page, attempt)
                try:
                    root = html.fromstring(self.get(url))

                    for exhibitor, subdomain in self.parse_exhibitor_list(root):
                        exhibitor_domain = subdomain
                        details_root = html.fromstring(self.get(exhibitor_domain))

                        title, name, tel, email = self.parse_exhibitor_details(details_root)

                        yield Exhibitor(exhibitor, title, name, tel, email, self.root + exhibitor_domain)

                    break

                except KeyboardInterrupt:
                    command = input('would you like to retry the current operation or exit the scraper? exit/[retry] ')
                    if command in ['exit', 'Exit']:
                        raise
                    else:
                        attempt = 0

                except Exception as e:
                    self.log.exception(e)
                    attempt += 1

            next_button = root.xpath("id('content')/div[3]/div[1]/div/div/a/span[@class='icon icon-next']")
            page += 1

        self.log.info('no more pages found')

    def parse_exhibitor_list(self, root):
        exhibitor_list = root.xpath("id('content')/div[3]/div[2]/div/ul/li")

        for entry in exhibitor_list:
            exhibitor = entry.xpath('div/div/p/a/text()')[0].replace('Aussteller:', '').strip()
            subdomain = entry.xpath('div/div/p/a/@href')[0]

            yield exhibitor, subdomain

    def parse_exhibitor_details(self, root):
        details = root.xpath("id('contacts')/div/div/div")[0]

        title = self.xpath_string(details, "id('contacts')/div/div/div/b/text()").strip()
        name  = self.xpath_string(details, "id('contacts')/div/div/div/em/text()").strip()
        email = self.xpath_string(details, "id('contacts')/div/div/div/a/@href").replace('mailto:','')
        tel   = ''

        text = self.xpath_string(details, "id('contacts')/div/div/div/text()", -1).strip()
        if 'Tel.:' in text:
            try:
                tel = re.match(r'Tel\.:\s+(.*)\n', text).groups()[0].strip()
            except: tel = text.strip()

        return title, name, tel, email

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 fenc=utf-8
