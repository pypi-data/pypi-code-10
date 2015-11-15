# -*- coding: utf-8 -*-

from .args import get_args
from .list import read_template, list_templates
from .dbus2xml import dbus2xml
from .xml2any import  xml2any

args = get_args()

xml = None

if args.list:
    list_templates()
elif not args.template:
    print('please choose a template:')
    print('-t TEMPLATE_NAME -x DBUS_XML')
    print('-t TEMPLATE_NAME -n BUS_NAME -p DBUS_PATH')
    print('Well know templates:')
    list_templates()
elif not args.xml and not args.busName:
    print('please inform a DBUS XML or DBUS NAME and PATH:')
    print('-t TEMPLATE_NAME -x DBUS_XML')
    print('-t TEMPLATE_NAME -n DBUS_NAME -p DBUS_PATH')
elif args.busName and not args.objectPath:
    print('please inform a DBUS NAME and PATH:')
    print('-t TEMPLATE_NAME -n DBUS_NAME -p DBUS_PATH')
elif args.xml:
    with open(args.xml) as xml_file:
        xml = xml_file.read()
elif args.busName and args.objectPath:
    xml = dbus2xml(args.busName, args.objectPath)

if xml:
    template = read_template(args.template)
    any = xml2any(template, xml, args)
    print(any)