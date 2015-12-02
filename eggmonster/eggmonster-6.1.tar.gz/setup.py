import sys

import setuptools

assert sys.version_info >= (2, 6), "eggmonster requires Python 2.6 or later"
py27 = sys.version_info >= (2, 7)
py26_reqs = ['argparse', 'importlib'] if not py27 else []

setup_params = dict(
    name='eggmonster',
    use_scm_version=True,
    author="Jamie Turner/YouGov",
    author_email="support@yougov.com",
    maintainer="YouGov",
    maintainer_email="support@yougov.com",
    url="https://bitbucket.org/yougov/eggmonster",
    packages=setuptools.find_packages(),
    install_requires=[
        "PyYAML >= 3.0.9",
        "yg.lockfile",
        "requests",
        "jaraco.collections",
        "jaraco.itertools",
        "jaraco.ui",
        ] + py26_reqs,
    extras_require=dict(
        server = [
            'yg.eventful>=2.0',
            'event>=0.4.2',
            ],
        ),
    entry_points = {
        'console_scripts': [
            'emget = eggmonster.emget:run',
            'emup = eggmonster.emup:run',
            "em = eggmonster.commands.em:run",
            "emi = eggmonster.commands.emi:run",
            "monster_debug = eggmonster.commands.monster_debug:run",
            "monster_eggserver = eggmonster.commands.monster_eggserver:run",
            "monster_launchd = eggmonster.commands.monster_launchd:run",
            "monster_logd = eggmonster.commands.monster_logd:run",
            "monster_run = eggmonster.commands.monster_run:run",
            "monster_server = eggmonster.commands.monster_server:run",
            "fake-monster = eggmonster.runner:FakeMonster.run",
        ],
    },
    setup_requires = [
        'setuptools_scm',
        'pytest-runner',
        ],
    use_2to3 = True,
    tests_require = [
        'pytest>=2.1',
        'dingus',
    ],
    classifiers = [
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
    ],
)

if __name__ == '__main__':
    setuptools.setup(**setup_params)
