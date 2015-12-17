# -*- coding: utf-8 -*-

"""Recipe thredds"""

import os
from mako.template import Template

import zc.buildout
from birdhousebuilder.recipe import conda, tomcat

wms_config = Template(filename=os.path.join(os.path.dirname(__file__), "wmsConfig.xml"))
thredds_config = Template(filename=os.path.join(os.path.dirname(__file__), "threddsConfig.xml"))
catalog_config = Template(filename=os.path.join(os.path.dirname(__file__), "catalog.xml"))

class Recipe(object):
    """This recipe is used by zc.buildout.
    It installs thredds with conda and setups thredds configuration."""

    def __init__(self, buildout, name, options):
        self.buildout, self.name, self.options = buildout, name, options
        b_options = buildout['buildout']
        self.prefix = self.options.get('prefix', conda.prefix())
        self.options['prefix'] = self.prefix
        self.options['data_root'] = options.get(
            'data_root', os.path.join(self.prefix, 'var', 'lib', 'pywps', 'outputs'))
        self.options['organisation'] = options.get('organisation', 'Birdhouse')
        self.options['website'] = options.get('website', '')
        self.options['allow_wms'] = options.get('allow_wms', 'true')
        self.options['allow_wcs'] = options.get('allow_wcs', 'false')
        self.options['allow_nciso'] = options.get('allow_nciso', 'false')

    def install(self, update=False):
        installed = []
        installed += list(self.install_tomcat(update))
        installed += list(self.install_conda(update))
        installed += list(self.install_thredds_config())
        installed += list(self.install_catalog_config())
        installed += list(self.install_wms_config())
        return installed

    def install_tomcat(self, update):
        script = tomcat.Recipe(
            self.buildout,
            self.name,
            self.options)
        return script.install(update)

    def install_conda(self, update=False):
        script = conda.Recipe(
            self.buildout,
            self.name,
            {'pkgs': 'thredds'})
        if update == True:
           return script.update()
        else:
           return script.install()

    def install_thredds_config(self):
        result = thredds_config.render(**self.options)

        output = os.path.join(tomcat.content_root(self.prefix), 'thredds', 'threddsConfig.xml')
        conda.makedirs(os.path.dirname(output))

        try:
            os.remove(output)
        except OSError:
            pass

        with open(output, 'wt') as fp:
            fp.write(result)
        return [output]

    def install_catalog_config(self):
        result = catalog_config.render(**self.options)

        output = os.path.join(tomcat.content_root(self.prefix), 'thredds', 'catalog.xml')
        conda.makedirs(os.path.dirname(output))

        try:
            os.remove(output)
        except OSError:
            pass

        with open(output, 'wt') as fp:
            fp.write(result)
        return [output]

    def install_wms_config(self):
        result = wms_config.render(**self.options)

        output = os.path.join(tomcat.content_root(self.prefix), 'thredds', 'wmsConfig.xml')
        conda.makedirs(os.path.dirname(output))

        try:
            os.remove(output)
        except OSError:
            pass

        with open(output, 'wt') as fp:
            fp.write(result)
        return [output]

    def update(self):
        return self.install(update=True)

def uninstall(name, options):
    pass

