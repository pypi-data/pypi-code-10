import fnmatch
import re
import subprocess
from contextlib import contextmanager
from glob import glob
from os import chdir, getcwd, lchown, makedirs, readlink, remove, symlink, walk
from os.path import (
    exists, isfile, join, splitext,
    abspath, basename, dirname, normpath, realpath, relpath)
from pwd import getpwnam
from shutil import copytree, rmtree
from tempfile import mkdtemp

from .exceptions import BadArchive, InvisibleRoadsError


def make_folder(folder):
    try:
        makedirs(folder)
    except OSError:
        pass
    return folder


def clean_folder(folder):
    remove_path(folder)
    return make_folder(folder)


def replace_folder(target_folder, source_folder):
    remove_path(target_folder)
    make_folder(dirname(target_folder))
    copytree(source_folder, target_folder)
    return target_folder


def remove_path(path):
    try:
        rmtree(path)
    except OSError:
        try:
            remove(path)
        except OSError:
            pass
    return path


def get_nickname(path):
    return splitext(basename(path))[0]


def make_link(source_path, target_path):
    source_path = normpath(source_path)
    if not exists(target_path):
        symlink(source_path, target_path)
        return target_path
    try:
        if normpath(readlink(target_path)) != source_path:
            raise IOError('could not make link; target_path is another link')
    except OSError:
        path_type = 'file' if isfile(target_path) else 'folder'
        raise IOError('could not make link; target_path is a %s' % path_type)
    return target_path


def find_path(name, folder):
    for root_folder, folder_names, file_names in walk(folder):
        if name in file_names:
            return join(root_folder, name)
    raise IOError('cannot find "%s" in "%s"' % (name, folder))


def find_paths(name_expression, folder):
    return [
        join(root_folder, file_name)
        for root_folder, folder_names, file_names in walk(folder)
        for file_name in fnmatch.filter(file_names, name_expression)]


def resolve_relative_path(relative_path, folder):
    relative_path = relpath(join(folder, relative_path), folder)
    if relative_path.startswith('..'):
        raise IOError('relative_path must refer to a file inside folder')
    return join(folder, relative_path)


def compress(source_folder, target_path=None):
    if not target_path:
        target_path = normpath(source_folder) + '.tar.gz'
    target_path = abspath(target_path)
    if target_path.endswith('.tar.gz'):
        command_terms = ['tar', 'czhf']
    else:
        command_terms = ['zip', '-r', '-9']
    with cd(source_folder):
        source_paths = glob('*')
        if not source_paths:
            raise IOError('cannot compress empty folder "%s"' % source_folder)
        subprocess.check_output(command_terms + [target_path] + source_paths)
    return target_path


def compress_zip(source_folder, target_path=None):
    if not target_path:
        target_path = source_folder + '.zip'
    return compress(source_folder, target_path)


def uncompress(source_path, target_folder=None):
    if source_path.endswith('.tar.gz'):
        command_terms = ['tar', 'xf', source_path, '-C']
        target_extension = '.tar.gz'
    else:
        command_terms = ['unzip', source_path, '-d']
        target_extension = '.zip'
    if not target_folder:
        target_folder = re.sub(
            target_extension.replace('.', '\.') + '$', '', source_path)
    make_folder(target_folder)
    try:
        subprocess.check_output(
            command_terms + [target_folder], stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as e:
        o = e.output
        if 'does not look like a tar archive' in o:
            m = 'could not unpack archive (source_path = %s)'
            raise BadArchive(m % source_path)
        raise InvisibleRoadsError(o)
    return target_folder


def are_same_path(path1, path2):
    return realpath(path1) == realpath(path2)


@contextmanager
def cd(target_folder):
    source_folder = getcwd()
    try:
        chdir(target_folder)
        yield
    finally:
        chdir(source_folder)


@contextmanager
def make_temporary_folder(suffix='', prefix='tmp', target_folder=None):
    temporary_folder = mkdtemp(suffix, prefix, target_folder)
    yield temporary_folder
    rmtree(temporary_folder)


def make_enumerated_folder_for(script_path, first_index=0):
    package_name = get_nickname(script_path)
    if 'run' == package_name:
        package_folder = dirname(abspath(script_path))
        package_name = get_nickname(package_folder)
    return make_enumerated_folder(join('/tmp', package_name), first_index)


def make_enumerated_folder(base_folder, first_index=0):
    suggest_folder = lambda x: join(base_folder, str(x))
    target_index = first_index
    target_folder = suggest_folder(target_index)
    while True:
        try:
            makedirs(target_folder)
            break
        except OSError:
            target_index += 1
            target_folder = suggest_folder(target_index)
    return target_folder


def change_owner_and_group_recursively(target_folder, target_username):
    'Change uid and gid of folder and its contents, treating links as files'
    pw_record = getpwnam(target_username)
    target_uid = pw_record.pw_uid
    target_gid = pw_record.pw_gid
    for root_folder, folders, names in walk(target_folder):
        for folder in folders:
            lchown(join(root_folder, folder), target_uid, target_gid)
        for name in names:
            lchown(join(root_folder, name), target_uid, target_gid)
    lchown(target_folder, target_uid, target_gid)
