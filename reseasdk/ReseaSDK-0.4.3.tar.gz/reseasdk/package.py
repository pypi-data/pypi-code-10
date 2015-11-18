import os
import glob
import subprocess
import urllib.request
import urllib.error
import yaml
from reseasdk.helpers import load_yaml
from reseasdk.validators import \
    validate_packages_yml, validate_package_yml, \
    validate_build_yml, validate_global_yml, ValidationError
from reseasdk.helpers import error


def get_path_from_packages_yml(package):
    yml = load_yaml('packages.yml', validator=validate_packages_yml)

    try:
        path = os.path.join(os.getcwd(), yml['packages'][package]['path'])
    except KeyError:
        return None

    return path


package_uris = {} # cache
PACKAGE_DB_URL = "https://raw.githubusercontent.com/resea/packages/master/{}.yml"
def _download_package(package):
    if package_uris.get(package) is None:
        # get package's URI from PACKAGE_DB_URI
        try:
            r = urllib.request.urlopen(PACKAGE_DB_URL.format(package))
            uri = yaml.safe_load(r)['uri']
        except urllib.error.HTTPError as e:
            error("failed to download package '{}': {}".format(package, str(e)))
        except KeyError:
            error("cannot download package '{}': uri not found in the package "
                  "database".format(package))

        # download the package
        scheme, repo = uri.split(':', 2)
        path = scheme + "-" + uri.replace('/', '-').replace(':', '-')
        if scheme == 'github':
            subprocess.check_output(['git', 'clone',
                                     'https://github.com/' + repo,
                                     path])
        else:
            error("cannot download package '{}': unknown uri scheme '{}'".format(
                  package, scheme))


def search_vendor_dir(package):
    # search .vendor directory
    cwd = os.getcwd()
    for d in glob.iglob('packages/.vendor/*'):
        os.chdir(d)
        path = get_path_from_packages_yml(package)
        os.chdir(cwd)
        if path:
            return path
    return None


def download_package(package):
    path = search_vendor_dir(package)
    if path:
        return path
    else:
        # download the package
        os.makedirs('packages/.vendor', exist_ok=True)
        os.chdir('packages/.vendor')
        _download_package(package)
        os.chdir('../..')
        path = search_vendor_dir(package)
        if path:
            return path
        else:
            error("failed to search for package '{}'".format(package))


current_package_name = None # cache
def get_package_dir(package):
    global current_package_name

    cwd = os.getcwd()

    # the current package
    if current_package_name is None:
        current_package_name = load_yaml('package.yml',
                                         validator=validate_package_yml).get('name')
    if current_package_name == package:
        return os.getcwd()

    # look for packages.yml
    while True:
        os.chdir("..")
        if os.getcwd() == "/":
            break
        if os.path.exists("packages.yml"):
            path = get_path_from_packages_yml(package)
            if path:
                os.chdir(cwd)
                return path
            # if not found in the packages.yml, look for its ancestor dirs

    # not found, download it
    os.chdir(cwd)
    return download_package(package)


def get_package(package):
    """ Prepare a package in 'packages' directory """

    if not os.path.exists('packages/' + package):
        os.makedirs('packages', exist_ok=True)
        path = get_package_dir(package)
        os.chdir('packages')
        os.symlink(path, package)
        os.chdir('..')


global_ymls = {}  # cache
def load_global_yml(package):
    if package in global_ymls:
        return global_ymls[package]

    get_package(package)
    try:
        yml = load_yaml('packages/{}/global.yml'.format(package),
                        validator=validate_global_yml)
    except FileNotFoundError:
        yml = {}
    global_ymls[package] = yml
    return yml


build_ymls = {}  # cache
def load_build_yml(package):
    if package in build_ymls:
        return build_ymls[package]

    get_package(package)
    try:
        yml = load_yaml('packages/{}/build.yml'.format(package),
                        validator=validate_build_yml)
    except FileNotFoundError:
        yml = {}
    build_ymls[package] = yml
    return yml


package_ymls = {}  # cache
def load_package_yml(package):
    if package in package_ymls:
        return package_ymls[package]

    get_package(package)
    yml = load_yaml('packages/{}/package.yml'.format(package),
                    validator=validate_package_yml)
    package_ymls[package] = yml
    return yml


def resolve_package_dependency(_packages, all_in_one, interfaces_only=False):
    """ Returns list of required packages. """
    packages = []
    follows = ['library']
    if all_in_one:
        follows.append('application')
    for package in _packages:
        yml = load_package_yml(package)
        packages += yml['implements']
        packages += yml['uses']
        for require in yml['requires'] + yml['implements'] + yml['uses']:
            if interfaces_only or \
               load_package_yml(require)['category'] in follows:
                packages += resolve_package_dependency([require], all_in_one,
                                                       interfaces_only=interfaces_only)
            packages.append(require)
        packages.append(package)
    return list(set(packages))


def filter_package_by_category(categories, packages):
    matched = []
    for package in packages:
        if load_package_yml(package)['category'] in categories:
            matched.append(package)
    return matched
