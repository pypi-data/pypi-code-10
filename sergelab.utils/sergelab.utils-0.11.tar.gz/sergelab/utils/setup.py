import fnmatch
import os
import shutil
import sys

from distutils.command.clean import clean as CleanCommand
from distutils.command.install import install as InstallCommand


def _findNremove(path, pattern, maxdepth=1):
    cpath = path.count(os.sep)

    for r, d, f in os.walk(path):
        if maxdepth == 0 or r.count(os.sep) - cpath < maxdepth:
            for files in f:
                if files.endswith(pattern):
                    try:
                        os.remove(os.path.join(r, files))
                    except Exception as e:
                        print(e)


class clean(CleanCommand):
    def run(self):
        shutil.rmtree(self.distribution.metadata.name + '.egg-info', True)
        shutil.rmtree('dist', True)
        shutil.rmtree('build', True)
        _findNremove('.', '.pyc', 0)
        CleanCommand.run(self)


class test_and_install(InstallCommand):
    def finalize_options(self):
        InstallCommand.finalize_options(self)
        self.single_version_externally_managed = None

    def run(self):
        path = os.getcwd()
        import nose.core
        test_success = nose.core.run(argv=sys.argv[:1], exit=False)
        os.chdir(path)

        if test_success:
            InstallCommand.do_egg_install(self)
        else:
            raise Exception("Tests failed.")


def find_package_data(package, src='', filter='*'):
    matches = []
    where = package.replace('.', os.sep)

    for root, dirnames, filenames in os.walk(os.path.join(where, src)):
        for filename in fnmatch.filter(filenames, filter):
            matches.append(os.path.relpath(os.path.join(root, filename), where))

    return {package: matches}
