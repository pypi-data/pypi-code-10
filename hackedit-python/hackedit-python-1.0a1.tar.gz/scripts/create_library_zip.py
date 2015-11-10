import os
import shutil

# packages to embed
import virtualenv
import rope


BUILD = os.path.abspath(os.path.join(os.getcwd(), '../build'))
ZIP = os.path.abspath(os.path.join(os.getcwd(), '../data/share/extlibs'))


def zipdir(source, destination):
    shutil.make_archive(destination, 'zip', source)


def embed_packages(packages):
    def copy_tree(src, dest):
        try:
            shutil.copytree(src, dest)
        except OSError:
            pass
        else:
            print('copied')

    destination = BUILD
    print('copy packages to build dir')
    for package in packages:
        print('copying package: %s' % package)
        if package.__file__.endswith('__init__.py'):
            # package
            src = os.path.dirname(package.__file__)
            dirname = os.path.split(os.path.dirname(package.__file__))[1]
            dest = os.path.join(destination, dirname)
            if 'pyqode' in package.__file__:
                dest = os.path.join(destination, 'pyqode', dirname)
            print('copying %s to %s' % (src, dest))
            copy_tree(src, dest)
            if 'pyqode' in package.__file__:
                with open(os.path.join(
                        destination, 'pyqode', '__init__.py'), 'w'):
                    pass
        else:
            # single module package, copy it directly
            src = package.__file__
            dest = destination
            print('copying %s to %s' % (src, dest))
            shutil.copy(src, dest)

    print('creating zip file')


def create_zip():
    zipdir(BUILD, ZIP)


try:
    os.mkdir(BUILD)
except FileExistsError:
    shutil.rmtree(BUILD)
    os.mkdir(BUILD)
embed_packages([virtualenv, rope])
create_zip()
