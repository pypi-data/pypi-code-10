#!/usr/bin/env python

from distutils.core import setup

setup(name = 'herculeum',
      version = '0.15',
      description = 'Small roguelike game',
      author = 'Tuukka Turto',
      author_email = 'tuukka.turto@oktaeder.net',
      url = 'https://github.com/tuturto/pyherc/',
      classifiers = ['Development Status :: 3 - Alpha',
                     'Environment :: Console :: Curses',
                     'Environment :: Win32 (MS Windows)',
                     'Environment :: X11 Applications :: Qt',
                     'Environment :: MacOS X',
                     'Intended Audience :: End Users/Desktop',
                     'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
                     'Natural Language :: English',
                     'Operating System :: OS Independent',
                     'Programming Language :: Python',
                     'Programming Language :: Python :: 3',
                     'Topic :: Games/Entertainment :: Role-Playing'],
      packages = ['herculeum',
                 'herculeum.ai',
                 'herculeum.config', 'herculeum.config.levels',
                 'herculeum.ui',
                 'herculeum.ui.controllers', 'herculeum.ui.gui', 'herculeum.ui.text',
                 'herculeum.ui.gui.animations',
                 'pyherc',
                 'pyherc.ai',
                 'pyherc.config', 'pyherc.config.dsl',
                 'pyherc.data', 'pyherc.data.effects', 'pyherc.data.features',
                 'pyherc.data.magic', 'pyherc.data.traps',
                 'pyherc.events',
                 'pyherc.generators', 'pyherc.generators.level',
                 'pyherc.generators.level.decorator', 'pyherc.generators.level.partitioners',
                 'pyherc.generators.level.room',
                 'pyherc.ports',
                 'pyherc.rules', 'pyherc.rules.combat', 'pyherc.rules.consume',
                 'pyherc.rules.digging',
                 'pyherc.rules.inventory', 'pyherc.rules.magic',
                 'pyherc.rules.waiting'],
      scripts = ['src/scripts/herculeum'],
      package_data={'herculeum': ['ai/*.hy',
                                  'config/*.hy',
                                  'config/levels/*.hy',                                  
                                  'ui/gui/animations/*.hy'],
                    'pyherc': ['*.hy',
                               'config/dsl/*.hy',
                               'data/*.hy',
                               'data/effects/*.hy',
                               'data/features/*.hy',
                               'data/traps/*.hy',
                               'events/*.hy',
                               'generators/*.hy',
                               'generators/level/*.hy',
                               'generators/level/decorator/*.hy',
                               'generators/level/partitioners/*.hy',
                               'generators/level/room/*.hy',
                               'rules/*.hy',
                               'rules/digging/*.hy',
                               'rules/metamorphosis/*.hy',
                               'rules/mitosis/*.hy',
                               'rules/moving/*.hy',
                               'rules/trapping/*.hy']},
      install_requires = ['decorator==3.4.0',
                          'hy==0.11.0',
                          'docopt==0.6.1'],
      package_dir = {'herculeum': 'src/herculeum',
                     'pyherc': 'src/pyherc'})
