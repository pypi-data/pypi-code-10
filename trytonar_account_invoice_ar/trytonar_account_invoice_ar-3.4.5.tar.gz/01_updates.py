#!/usr/bin/env python2
# -*- encoding: utf-8 -*-
#
# this file is part of the cultura-tryton package for tryton.
# the COPYRIGHT file at the top level of this repository
# contains the full copyright notice and license terms.


# Imports
from optparse import OptionParser
from proteus import Model
from proteus import config as pconfig

def main(options):

    config = pconfig.set_trytond(options.database, password=options.admin_pwd,
        config_file=options.config_file)

    Lang = Model.get('ir.lang')
    (es_AR,) = Lang.find([('code', '=', 'es_AR')])
    es_AR.translatable = True
    es_AR.save()

    update_menu(config, es_AR)
    update_config_party(config, es_AR)
    print "done."

def update_menu(config, lang):
    """ Ocultar items de menu. """
    Menu = Model.get('ir.ui.menu')

    print u'\n>>> Buscar menus a ocultar...'
    menu, = Menu.find([('name', '=', u'Facturas'), ('icon', '=', 'tryton-list')])
    menu.active = False
    menu.save()

    menu, = Menu.find([('name', '=', u'Notas de cr\xe9dito'), ('icon', '=', 'tryton-list')])
    menu.active = False
    menu.save()
    print u'\n>>> update_menu done.'

def update_config_party(config, lang):
    """ Seteamos el idioma de la entidad 'Spanish Argentina' por defecto. """
    PartyConfig = Model.get('party.configuration')

    print u'\n>>> Idioma de la entidad por defecto es Spanish Argentina...'
    party_config = PartyConfig([])
    party_config.party_lang = lang
    party_config.save()

if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option('-d', '--database', dest='database')
    parser.add_option('-c', '--config-file', dest='config_file')
    parser.add_option('-a', '--admin-pwd', dest='admin_pwd')
    parser.add_option('-l', '--host', dest='host')
    parser.set_defaults(user='admin')

    options, args = parser.parse_args()
    if args:
        parser.error('Parametros incorrectos')
    if not options.database:
        parser.error('Se debe definir [nombre] de base de datos')
    if not options.config_file:
        parser.error(u'Se debe definir el path absoluto al archivo de configuración de trytond')
    if not options.admin_pwd:
        parser.error(u'Se debe definir password del usuario admin')
    if not options.host:
        parser.error(u'Debe definir host de conexión a base de datos Postgres')

    main(options)
