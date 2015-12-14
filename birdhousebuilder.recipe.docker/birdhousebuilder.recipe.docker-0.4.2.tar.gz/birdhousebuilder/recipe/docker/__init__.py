# -*- coding: utf-8 -*-

"""Recipe docker"""

import os
from mako.template import Template

templ_dockerfile = Template(filename=os.path.join(os.path.dirname(__file__), "Dockerfile"))

class Recipe(object):
    """Buildout recipe to generate a Dockerfile."""

    def __init__(self, buildout, name, options):
        self.buildout, self.name = buildout, name
        b_options = buildout['buildout']
        self.buildout_dir = b_options.get('directory')

        self.options = dict()
        self.options['image_name'] = options.get('image-name', 'birdhouse/bird-base')
        self.options['image_version'] = options.get('image-version', 'latest')
        self.options['maintainer'] = options.get('maintainer', 'https://github.com/bird-house')
        self.options['description'] = options.get('description', 'Birdhouse Application')
        self.options['vendor'] = options.get('vendor', 'Birdhouse')
        self.options['version'] = options.get('version', '1.0.0')
        self.options['source'] = options.get('source', '.')
        self.options['git_url'] = options.get('git-url')
        self.options['git_branch'] = options.get('git-branch', 'master')
        self.options['subdir'] = options.get('subdir')
        self.options['buildout_cfg'] = options.get('buildout-cfg')
        self.options['expose'] = ' '.join([port for port in options.get('expose', '').split() if port])
        envs = [env for env in options.get('environment', '').split() if env]
        self.options['environment'] = {k:v for k,v in (env.split('=') for env in envs) }

    def install(self):
        installed = []
        installed += list(self.install_dockerfile())
        return installed

    def install_dockerfile(self):
        result = templ_dockerfile.render(**self.options)
        output = os.path.join(self.buildout_dir, 'Dockerfile')
        
        try:
            os.remove(output)
        except OSError:
            pass

        with open(output, 'wt') as fp:
            fp.write(result)
            os.chmod(output, 0o644)
        return [output]

    def update(self):
        return self.install()

def uninstall(name, options):
    pass

