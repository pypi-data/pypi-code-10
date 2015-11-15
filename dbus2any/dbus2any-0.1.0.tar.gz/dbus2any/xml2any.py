# -*- coding: utf-8 -*-
from jinja2 import Template
import xml.etree.ElementTree as ET


def xml2any(tpl, xml, args=None):
    node = ET.fromstring(xml)
    template = Template(tpl)
    arg = {}
    if args:
        arg = {
                'template': args.template,
                'xml': args.xml,
                'busName': args.busName,
                'objectPath': args.objectPath,
                'interface': args.interface
            }
    return template.render(node=node,
        args=arg)
