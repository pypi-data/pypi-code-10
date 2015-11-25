# -*- coding: utf-8 -*-
#
# Copyright (C) 2015, Maximilian Köhl <mail@koehlma.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import os
import os.path
import platform
import shutil
import subprocess
import sys

from distutils import log
from distutils.command.build_ext import build_ext
from distutils.errors import DistutilsError

from setuptools import setup


import cffi

__dir__ = os.path.dirname(__file__)


with open(os.path.join(__dir__, 'cffi_source.c')) as cffi_source:
    source = cffi_source.read()

with open(os.path.join(__dir__, 'cffi_declarations.c')) as cffi_declarations:
    declarations = cffi_declarations.read()

ffi = cffi.FFI()
ffi.set_source('_uv', source)
ffi.cdef(declarations)

extension = ffi.distutils_extension()

WIN32_LIBRARIES = ['libuv', 'advapi32', 'iphlpapi', 'psapi',
                   'shell32', 'userenv', 'ws2_32']

WIN32_PYTHON27_PATHS = [r'C:\Program Files (x86)\Python 2.7\python.exe',
                        r'C:\Python27\python.exe']


def choose_path(paths):
    for path in paths:
        if os.path.exists(path):
            return path


def win32_find_python27():
    assert sys.platform == 'win32'
    if 'PYTHON' in os.environ:
        python27 = os.environ['PYTHON']
    else:
        python27 = choose_path(WIN32_PYTHON27_PATHS)
    if not python27 or not os.path.isfile(python27):
        raise RuntimeError('python 2.7 interpreter not found')
    cmd = [python27, '--version']
    stderr = subprocess.STDOUT
    version = subprocess.check_output(cmd, stderr=stderr)[7:].decode().strip()
    if not version.startswith('2.7'):
        raise RuntimeError('python 2.7 interpreter not found')
    return python27


def win32_build_environ():
    environ = dict(os.environ)
    environ['PYTHON'] = win32_find_python27()
    return environ


class BuildExtensions(build_ext):
    libuv_path = os.path.join('build', 'libuv')
    libuv_repo = 'https://github.com/libuv/libuv.git'
    libuv_branch = 'v1.x'
    libuv_tag = 'v1.7.5'

    user_options = build_ext.user_options[:]
    user_options.extend([
        ('libuv-build-clean', None, 'Clean LibUV tree before compilation.'),
        ('libuv-force-fetch', None, 'Remove LibUV (if present) and fetch it again.'),
        ('use-system-libuv', None, 'Use the system provided version of LibUV.')
    ])

    boolean_options = build_ext.boolean_options[:]
    boolean_options.extend(['libuv-build-clean', 'libuv-force-fetch',
                            'libuv-verbose-build', 'use-system-libuv'])

    def __init__(self, dist):
        build_ext.__init__(self, dist)
        self.libuv_build_clean = False
        self.libuv_force_fetch = False
        self.use_system_libuv = False

    def initialize_options(self):
        self.libuv_build_clean = False
        self.libuv_force_fetch = False
        self.use_system_libuv = False
        build_ext.initialize_options(self)

    def build_extensions(self):
        if sys.platform.startswith('linux'):
            extension.libraries.append('rt')
        elif sys.platform == 'win32':
            self.compiler.add_library_dir(os.path.join(self.libuv_path, 'Release', 'lib'))
            extension.libraries.extend(WIN32_LIBRARIES)
            extension.define_macros.append(('WIN32', 1))
            extension.extra_link_args.extend(['/NODEFAULTLIB:libcmt', '/LTCG'])
        elif sys.platform.startswith('freebsd'):
            extension.libraries.append('kvm')

        if self.use_system_libuv:
            if sys.platform == 'win32':
                msg = 'using a system provided LibUV is unsupported on Windows'
                raise DistutilsError(msg)
            extension.libraries.append('uv')
        else:
            self.use_own_libuv()

        build_ext.build_extensions(self)

    def use_own_libuv(self):
        if self.libuv_force_fetch:
            shutil.rmtree(self.libuv_path)

        if not os.path.exists(self.libuv_path):
            try:
                self.clone_libuv()
            except Exception:
                shutil.rmtree(self.libuv_path)
                raise

        if self.libuv_build_clean:
            self.clean_libuv()

        self.build_libuv()

        self.compiler.add_include_dir(os.path.join(self.libuv_path, 'include'))
        if sys.platform != 'win32':
            libuv_lib = os.path.join(self.libuv_path, '.libs', 'libuv.a')
            extension.extra_objects.append(libuv_lib)

    def clone_libuv(self):
        log.info('Cloning LibUV...')
        cmd = ['git', 'clone', '-b', self.libuv_branch, self.libuv_repo, self.libuv_path]
        subprocess.check_call(cmd)
        subprocess.check_call(['git', 'checkout', self.libuv_tag], cwd=self.libuv_path)

    def build_libuv(self):
        log.info('Building LibUV...')
        if sys.platform == 'win32':
            self.build_libuv_win32()
            return

        subprocess.check_call(['sh', 'autogen.sh'], cwd=self.libuv_path)
        subprocess.check_call(['./configure'], cwd=self.libuv_path)
        subprocess.check_call(['make'], cwd=self.libuv_path)

    def build_libuv_win32(self):
        architecture = {'32bit': 'x86', '64bit': 'x64'}[platform.architecture()[0]]
        cmd = ['vcbuild.bat', architecture, 'release']
        env = win32_build_environ()
        subprocess.check_call(cmd, shell=True, cwd=self.libuv_path, env=env)

    def clean_libuv(self):
        if sys.platform == 'win32':
            self.clean_libuv_win32()
            return

        subprocess.check_call(['make', 'clean'], cwd=self.libuv_path)
        subprocess.check_call(['make', 'distclean'], cwd=self.libuv_path)

    def clean_libuv_win32(self):
        log.info('Cleaning LibUV...')
        cmd = ['vcbuild.bat', 'clean']
        env = win32_build_environ()
        subprocess.check_call(cmd, shell=True, cwd=self.libuv_path, env=env)


setup(name='uv',
      version='0.0.2dev1',
      description='Python LibUV',
      author='Maximilian Köhl',
      author_email='mail@koehlma.de',
      url='https://www.koehlma.de/projects/uv/',
      packages=['uv'],
      cmdclass={'build_ext': BuildExtensions},
      ext_modules=[extension])
