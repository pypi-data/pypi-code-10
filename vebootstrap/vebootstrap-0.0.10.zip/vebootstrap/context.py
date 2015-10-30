# -*- coding: utf-8 -*-
import os
from os import path
import sys
import shutil
import subprocess
from . import config


class Context(object):

    REQUIREMENTS = "requirements.txt"

    def __init__(self, python_exe, script_path):
        self.config = config.Config()
        self.script_path = path.abspath(script_path)
        self.script_dir = path.dirname(self.script_path)
        self.python_exe = path.abspath(python_exe)
        self.pyvenv_dir = path.join(self.script_dir,
                ".py{0}{1}".format(sys.version_info[0], sys.version_info[1]))
        self.current_requirements = path.join(self.script_dir, self.REQUIREMENTS)
        self.last_requirements = path.join(self.pyvenv_dir, self.REQUIREMENTS)

        # os detection
        if os.name == 'nt':
            self.bin_path = path.join(self.pyvenv_dir, "Scripts")
            self.path_separator = ";"
            # In order to enable PATH environment
            self.shell = True
        else:
            self.bin_path = path.join(self.pyvenv_dir, "bin")
            self.path_separator = ":"
            self.shell = False

        # version detection
        if sys.version_info[0] == 2:
            self.virtualenv = "virtualenv"
        else:
            self.virtualenv = "venv"

    def create_venv(self):
        if self.shell_execute([self.python_exe, "-m", self.virtualenv, self.pyvenv_dir]) != 0:
            raise Exception("cannot create virtualenv")

        if not os.access(self.current_requirements, os.F_OK):
            open(self.current_requirements, "wb").close()

    def pip_install(self):
        shutil.copy(self.current_requirements, self.last_requirements)

        # default install
        for p in self.config.default_packages:
            self.activate_venv(["pip", "install", p])

        # requirements install
        self.activate_venv(["pip", "install", "-r", self.current_requirements])

    def pywin_install(self):
        import tempfile
        from . import pywinpackage

        temp_dir = path.join(tempfile.gettempdir(), "vebootstrap_pywinpackage")
        pywin = pywinpackage.PyWinPackages(temp_dir)

        # default install
        for i, p in enumerate(self.config.default_windows_packages):
            print("PyWinPackages Collecting {} (from default_windows_packages {} (index {}))".format(p,
                self.config.FILENAME, i))
            filename = pywin.download(p)
            self.activate_venv(["pip", "install", filename])

        # requirements install
        win_packages = pywinpackage.parse_requirements(self.current_requirements)
        if not os.access(temp_dir, os.F_OK):
            os.makedirs(temp_dir)
        for line_num, p in win_packages:
            print("PyWinPackages Collecting {} (from -r {} (line {}))".format(p,
                self.current_requirements, line_num))
            filename = pywin.download(p)
            self.activate_venv(["pip", "install", filename])

    def pip_uninstall(self):
        self.activate_venv(["pip", "uninstall", "-r", self.last_requirements, "-y"])

    def should_update_packages(self):
        def get_updated_time(filename):
            from datetime import datetime
            stat = os.stat(filename)
            return stat.st_mtime

        if not os.access(self.last_requirements, os.F_OK) or \
                not os.access(self.current_requirements, os.F_OK):
            return False

        old_package_updated_time = get_updated_time(self.last_requirements)
        new_package_updated_time = get_updated_time(self.current_requirements)
        return old_package_updated_time < new_package_updated_time

    def activate_venv(self, cmd):
        return self.shell_execute(cmd, {
                "PATH": self.bin_path + self.path_separator + os.environ['PATH'],
                "VIRTUAL_ENV": self.pyvenv_dir
                })

    def bootstrap(self, args):
        BOOTSTRAP_OPTION = "--VEBOOTSTRAPPED-V8guR5ySAymI"
        if BOOTSTRAP_OPTION in sys.argv:
            sys.argv.remove(BOOTSTRAP_OPTION)
            return

        self.start(args + [BOOTSTRAP_OPTION])

    def start(self, args):
        self.setup()
        sys.exit(self.activate_venv(["python", self.script_path] + args))

    def setup(self):
        if self.should_update_packages():
            shutil.rmtree(self.pyvenv_dir)

        if not os.access(self.pyvenv_dir, os.F_OK):
            try:
                self.create_venv()
                self.pip_install()
                if os.name == 'nt':
                    self.pywin_install()
                return True
            except BaseException as e:
                sys.stderr.write("Rolling back...")
                if os.access(self.pyvenv_dir, os.F_OK):
                    shutil.rmtree(self.pyvenv_dir)
                sys.stderr.write("done\n")
                raise e
        return False

    def shell_execute(self, cmd, env={}, stdout=None):
        return subprocess.call(cmd, env=dict(os.environ, **env), shell=self.shell, stdout=stdout)

