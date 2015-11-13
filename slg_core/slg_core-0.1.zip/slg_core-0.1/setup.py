from setuptools import setup
from pip.req import parse_requirements
import pip

from setuptools_behave import behave_test
from setuptools import Command
from distutils import dir_util
from fnmatch import fnmatch
import os.path
import sys
import shlex
import subprocess


class custom_behave_test(behave_test):

    def behave(self, path):
        behave = os.path.join("bin", "behave")
        if not os.path.exists(behave):
            behave = "behave.exe"
        cmd_options = ""
        if self.tags:
            cmd_options = "--tags=" + " --tags=".join(self.tags)
        if self.dry_run:
            cmd_options += " --dry-run"
        cmd_options += " --format=%s %s" % (self.format, path)
        self.announce("CMDLINE: %s %s" % (behave, cmd_options), level=3)

        # Had to sub class and override this method:
        # return subprocess.call([sys.executable, behave] + shlex.split(cmd_options))
        return subprocess.call([behave] + shlex.split(cmd_options))

# session=pip.download.PipSession() required due to pip versioning
parse_install_reqs = parse_requirements('requirements.txt', session=pip.download.PipSession())
parse_test_reqs = parse_requirements('requirements-tests.txt', session=pip.download.PipSession())

install_reqs = [str(ir.req) for ir in parse_install_reqs]
test_reqs = [str(tr.req) for tr in parse_test_reqs]

setup(
    name='slg_core',
    version='0.1',
    description='Slingshot Core Framework',
    url='http://git.prod.skyscanner.local/slingshot/slingshot-core.git',
    packages=['core'],
    install_requires=install_reqs,
    tests_require=test_reqs,
    cmdclass = {
        "test": custom_behave_test,
    },
)
