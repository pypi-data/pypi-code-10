"""
This module contains the compiler interface that is used to compile a file
following a given configuration.
"""
import json
import shutil
import glob
import sys
import locale
import logging
import os
import re
import tempfile

from PyQt5 import QtCore

from pyqode.core.modes import CheckerMessage, CheckerMessages

from hackedit import api
from hackedit.api import system
from hackedit_cobol.lib import msvc, utils


#: Executable file type
EXECUTABLE = 0
#: Module file type
MODULE = 1


#: Name for the default config
DEFAULT_CONFIG_NAME = 'Default'


#: Define the default/builtin compiler configuration.
DEFAULT_CONFIG = {
    'name': DEFAULT_CONFIG_NAME,
    'cobc': api.system.which('cobc'),
    'cobcrun': api.system.which('cobcrun'),
    'environment': {
        'COB_CONFIG_DIR': os.environ.get('COB_CONFIG_DIR', ''),
        'COB_COPY_DIR': os.environ.get('COB_COPY_DIR', ''),
        'COB_LIB_PATH': os.environ.get('COB_LIB_PATH', ''),
    },
    'output-directory': 'build',
    'standard': 'default',
    'free-format': False,
    '-static': False,
    '-debug': True,
    '-g': False,
    '-ftrace': False,
    '-ftraceall': False,
    '-fdebugging-line': False,
    'copybook-paths': [],
    'library-paths': [],
    'libraries': [],
    'extra-compiler-flags': [],
    'vcvarsall': '',
    'vcvarsall-arch': 'x86',
    'module-extension': '.dll' if system.WINDOWS else '.so'
                        if system.LINUX else '.dylib',
    'executable-extension': '.exe' if system.WINDOWS else ''
}


def check_config(config):
    """
    Checks if config is valid (if the compiler path can be found).
    """
    return os.path.exists(config['cobc']) and os.path.exists(config['cobcrun'])


def get_default_config():
    """
    Gets the default compiler configuration.
    """
    return QtCore.QSettings().value(
        'cobol/default_config', DEFAULT_CONFIG_NAME)


def set_default_config(name):
    """
    Sets the default compiler configuration.
    """
    return QtCore.QSettings().setValue(
        'cobol/default_config', name)


def get_compiler_configs():
    """
    Gets the list of compiler configurations.
    """
    configs = json.loads(QtCore.QSettings().value(
        'cobol/compiler_configs', '[]'))
    sanitized = []
    for cfg in configs:
        if cfg['name'] == 'Default':
            continue
        sanitized.append(cfg)
    sanitized.append(update_default_config())
    return sanitized


def set_configs(configs):
    """
    Saves the list of compiler configurations.
    """
    sanitized = []
    for cfg in configs:
        if cfg['name'] == 'Default':
            continue
        sanitized.append(cfg)
    configs = json.dumps(sanitized)
    QtCore.QSettings().setValue('cobol/compiler_configs', configs)


def get_compiler_config(cfg_name):
    """
    Gets the specified compiler config or None if the config name does not
    exist.
    """
    for cfg in get_compiler_configs():
        if cfg and cfg['name'] == cfg_name:
            return cfg
    return None


def get_compiler_config_names():
    """
    Get the list of the names of the existing compiler configurations.
    """
    return [cfg['name'] for cfg in get_compiler_configs() if cfg]


def update_default_config():
    update = {
        'cobc': api.system.which('cobc'),
        'cobcrun': api.system.which('cobcrun'),
        'environment': {
            'COB_CONFIG_DIR': os.environ.get('COB_CONFIG_DIR', ''),
            'COB_COPY_DIR': os.environ.get('COB_COPY_DIR', ''),
            'COB_LIB_PATH': os.environ.get('COB_LIB_PATH', '')
        },
    }

    if api.system.WINDOWS:
        # try using OpenCobolIDE's bundled compiler for now...
        # todo: use our own bundled compiler when alpha 2 has been released
        path = r'C:\Program Files (x86)\OpenCobolIDE\GnuCOBOL\bin\cobc.exe'
        if os.path.exists(path):
            update['cobc'] = path
            update['cobcrun'] = 'cobcrun.exe'

        if os.path.exists(update['cobc']):
            current = os.path.dirname(update['cobc'])
            parent = os.path.abspath(os.path.join(current, '..'))

            for varname, dirname in [
                    ('COB_CONFIG_DIR', 'config'), ('COB_COPY_DIR', 'copy'),
                    ('COB_LIB_PATH', 'lib')]:
                if not update['environment'][varname]:
                    for directory in [current, parent]:
                        path = os.path.join(directory, dirname)
                        if os.path.exists(path):
                            update['environment'][varname] = path
                            break

    DEFAULT_CONFIG.update(update)

    return DEFAULT_CONFIG


class GnuCOBOLCompiler:
    """
    Interfaces to the GnuCOBOL compiler.
    """
    _FILE_EXTENSIONS = {
        # Executable
        True: '.exe' if system.WINDOWS else '',
        # Module
        False:
            '.dll' if system.WINDOWS else '.so' if system.LINUX else '.dylib'
    }

    CRASH_CODE = 139

    TEST_CODE = '''       IDENTIFICATION DIVISION.
       PROGRAM-ID. HELLO.
       PROCEDURE DIVISION.
       MAIN-PROCEDURE.
            DISPLAY "Hello world"
            STOP RUN.
       END PROGRAM HELLO.
'''

    # GC output messages format depends on the underlying compiler
    # See https://github.com/OpenCobolIDE/OpenCobolIDE/issues/206
    OUTPUT_PATTERN_GCC = re.compile(
        r'^(?P<filename>[\w\.\-_\s]*):(?P<line>\s*\d*):(?P<level>[\w\s]*):'
        r'(?P<msg>.*)$')

    OUTPUT_PATTERN_MSVC = re.compile(
        r'^(?P<filename>[\w\.\-_\s]*)\((?P<line>\s*\d*)\):(?P<level>[\w\s]*):'
        '(?P<msg>.*)$')

    OUTPUT_PATTERNS = [OUTPUT_PATTERN_GCC, OUTPUT_PATTERN_MSVC]

    VERSION_PATTERN = re.compile(r'cobc \([\w\s]*\)\s(?P<version>.*)')

    def __init__(self, config):
        """
        Creates a compiler instance for a given configuration.

        :param config: compiler configuration.
        """
        self.config = config
        try:
            self.extensions = {
                # Executable
                True: config['executable-extension'],
                # Module
                False: config['module-extension']
            }
        except KeyError:
            self.extensions = self._FILE_EXTENSIONS.copy()

    @staticmethod
    def get_file_type(path):
        """
        Detects file type. If the file contains 'PROCEDURE DIVISION USING',
        then it is considered as a module else it is considered as an
        executable.

        :param path: file path
        :return: EXECUTABLE (0) or MODULE (1)
        """
        encoding = utils.get_file_encoding(path)
        _logger().debug('detecting file type: %s - %s', path, encoding)
        ftype = EXECUTABLE
        try:
            with open(path, 'r', encoding=encoding) as f:
                content = f.read().upper()
        except UnicodeDecodeError:
            return None
        if re.match(r'.*PROCEDURE[\s\n]+DIVISION[\s\n]+USING', content,
                    re.DOTALL):
            ftype = MODULE
        return ftype

    def get_cobc_info(self):
        if not self.config['cobc']:
            return 'Cannot run cobc --info, invalid compiler path'
        status, output = self.run_command(
            self.config['cobc'], ['--info'], os.getcwd())
        if status != 0:
            output = 'Command not supported by the compiler (only recent ' \
                'builds of GnuCOBOL have cobc --info.)\n\nProcess output: %s' \
                % output
        return output

    def get_cobcrun_runtime_env(self):
        if not self.config['cobcrun']:
            return 'Cannot run cobcrun --runtime-env, invalid path...'
        status, output = self.run_command(
            self.config['cobcrun'], ['--runtime-env'], os.getcwd())
        if status != 0:
            output = 'Command not supported by the module runner (only recent'\
                ' builds of GnuCOBOL have cobcrun --runtime-env.)\n\n' \
                'Process output: %s' % output
        return output

    @classmethod
    def get_version(cls, config, include_all=False):
        """
        Gets the compiler version for the given config.

        :param config: Config to get versionf from
        :param include_all: Include all version output of keep just the most
            significant parts.
        """
        if cls.check_config(config):
            status, output = cls(config).run_command(
                config['cobc'], ['--version'], '')
            if status == 0 and output:
                if include_all:
                    return output
                else:
                    for l in output.splitlines():
                        m = cls.VERSION_PATTERN.match(l)
                        if m:
                            return m.group('version')
        return 'Compiler not found'

    @classmethod
    def check_config(cls, config):
        """
        Checks config for invalid compiler path.
        """
        if config['cobc']:
            try:
                return os.path.exists(cls(config).get_full_compiler_path())
            except TypeError:
                pass
        return False

    @classmethod
    def check_compiler(cls, config):
        """
        Checks the compiler configuration `config` by compiling a simple
        hello world example executable.
        """
        def get_output_path(input_path):
            dirname, filename = os.path.split(input_path)
            basename = os.path.splitext(filename)[0]
            possible_extensions = ['.exe', '.dll', '.so', '.dylib']
            for ext in possible_extensions:
                candidate = os.path.join(dirname, basename + ext)
                if os.path.exists(candidate):
                    return candidate
            return None

        _logger().info('check compiler config: %r', config)
        if cls.check_config(config):
            _logger().debug('testing configuration %r' % config)
            compiler = GnuCOBOLCompiler(config)
            # create HelloWorld.cbl in /tmp
            working_dir = tempfile.gettempdir()
            path = os.path.join(working_dir, 'test.cbl')
            with open(path, 'w') as f:
                f.write(cls.TEST_CODE)

            std_args = []
            standard = config['standard']
            if standard.lower() != 'none':
                std_args = ['-std', config['standard']]

            exit_status, output = compiler.run_command(
                compiler.config['cobc'], std_args + ['-x', path],
                working_dir=working_dir)
            dest = get_output_path(path)
            if dest:
                try:
                    os.remove(dest)
                except OSError:
                    pass

            try:
                os.remove(path)
            except PermissionError:
                pass
            return exit_status, output
        else:
            return 1, 'Invalid compiler path: %s' % config['cobc']

    @classmethod
    def is_working(cls, config):
        ret, output = cls.check_compiler(config)
        return ret == 0

    def get_output_path(self, in_path, out_dir=None, executable=False):
        """
        Gets the absolute output path for a given cobol file path.
        """
        in_path = os.path.normpath(in_path)
        working_dir = os.path.dirname(in_path)
        abs_out_path, rel_out_path = self._get_output_path(
            in_path, out_dir, executable, working_dir)
        return abs_out_path

    def setup_environment(self):
        env = QtCore.QProcessEnvironment()

        for k, v in os.environ.items():
            if k != 'PATH':
                env.insert(k, v)

        PATH = os.environ['PATH']

        # Retrieve msvc environment vars if needed
        if self.config['vcvarsall']:
            vc_vars = msvc.query_vars(self.config['vcvarsall'],
                                      self.config['vcvarsall-arch'])
            for k, v in vc_vars.items():
                if k != 'PATH':
                    env.insert(k, v)
                else:
                    # we can safely replace original env by the one returned
                    # by vcvarsall as it includes what is defined in our
                    # process
                    PATH = v

        # Set environment variables defined in the compiler config
        for k, v in self.config['environment'].items():
            if not v:
                continue
            if k == 'PATH':
                PATH = v + os.pathsep + PATH
            if env.contains(k):
                value = env.value(k)
                v = v + os.pathsep + value
            env.insert(k, v)

        # Prepend compiler path
        compiler_path = self.get_full_compiler_path()
        if compiler_path and os.path.exists(compiler_path):
            compiler_dir = os.path.dirname(compiler_path)
            PATH = compiler_dir + os.pathsep + PATH

        env.insert('PATH', PATH)
        return env

    def get_full_compiler_path(self):
        compiler_path = self.config['cobc']
        if not os.path.isabs(compiler_path) and compiler_path:
            PATH = os.environ['PATH']
            if 'PATH' in self.config['environment']:
                cobc_path = self.config['environment']['PATH']
                PATH = cobc_path + os.pathsep + PATH
            compiler_path = system.which(compiler_path, path=PATH)
        if compiler_path is None:
            return None
        return os.path.normpath(compiler_path)

    def _prepare_bin_dir(self, output_dir):
        """
        On Windows, copy the compiler runtime dlls in the output dir.

        This is done so that users can run the executable directly from the
        file explorer and make deployement easy.
        """
        if sys.platform == "win32":
            # copy the dll
            files = glob.glob(os.path.join(
                os.path.dirname(self.get_full_compiler_path()), "*.dll"))
            for f in files:
                shutil.copy(f, output_dir)

    def compile_file(self, in_path, out_dir=None, executable=True):
        """
        Compiles `in_path` to `out_dir` according to the configuration
        set when the compiler instance was created.

        :param in_path: input file path
        :param out_dir: output directory. If None, the output will be deduced
            from the compiler configuration's output directory.
        :param executable: True for an executable, False for a module.

        :raises: ValueError if in_path does not exists. Might also raise an
            OSError if the output file is read-only.

        :returns: command, status, output, absolute_output_file_path
        """

        if not os.path.exists(in_path):
            raise ValueError('Input file (%r) does not exist' % in_path)

        # get working paths
        in_path = os.path.normpath(in_path)
        working_dir = os.path.dirname(in_path)
        rel_in_path = os.path.split(in_path)[1]
        working_dir = os.path.dirname(in_path)
        abs_out_path, rel_out_path = self._get_output_path(
            in_path, out_dir, executable, working_dir)
        pgm, args = self._make_cobc_command(
            rel_in_path, rel_out_path, executable)

        # create destination directories if missing
        dirname = os.path.dirname(abs_out_path)
        if not os.path.exists(dirname):
            os.makedirs(dirname)

        # check for potential permission errors
        if not os.access(dirname, os.W_OK):
            raise OSError('PermissionError: build directory is read-only')
        command = '%s %s' % (pgm, ' '.join(args))
        if os.path.exists(abs_out_path) and not os.access(
                abs_out_path, os.W_OK):
            raise OSError('PermissionError: %s is read-only' %
                          abs_out_path)

        # check modification time to see if the compilation is really needed
        if not check_mtime(in_path, abs_out_path):
            return command, 0, 'Compilation skipped, up to date...', \
                abs_out_path

        # self._prepare_bin_dir(os.path.dirname(abs_out_path))

        _logger().info('compiling %s', in_path)
        _logger().debug('output path: %s' % abs_out_path)
        status, output = self.run_command(pgm, args, working_dir)

        if status == 0 and not os.path.exists(abs_out_path):
            output = 'Compilation process exited with exit status 0 but ' \
                'output file does not exists.\nCompiler output:\%s' % output
            status = 1

        return command, status, output, abs_out_path

    def run_command(self, pgm, args, working_dir):
        if not pgm:
            return None

        original_path = os.environ['PATH']

        # make sure to add quotes arround a path that contains spaces
        if ' ' in pgm:
            pgm = '"%s"' % pgm

        p_env = self.setup_environment()
        os.environ['PATH'] = p_env.value('PATH')
        process = QtCore.QProcess()
        process.setWorkingDirectory(working_dir)
        process.setProcessChannelMode(QtCore.QProcess.MergedChannels)
        process.setProcessEnvironment(p_env)

        _logger().debug('command: %s', ' '.join([pgm] + args))
        _logger().debug('environment: %r',
                        process.processEnvironment().toStringList())

        process.start(pgm, args)
        process.waitForFinished()

        # determine exit code (handle crashed processes)
        if process.exitStatus() != process.Crashed:
            status = process.exitCode()
        else:
            status = self.CRASH_CODE

        # get compiler output
        raw_output = process.readAllStandardOutput().data()
        try:
            output = raw_output.decode(
                locale.getpreferredencoding()).replace('\r', '')
        except UnicodeDecodeError:
            # This is a hack to get a meaningful output when compiling a file
            # from UNC path using a batch file on some systems, see
            # https://github.com/OpenCobolIDE/OpenCobolIDE/issues/188
            output = str(raw_output).replace("b'", '')[:-1].replace(
                '\\r\\n', '\n').replace('\\\\', '\\')

        _logger().debug('exit code: %d' % status)
        _logger().debug('output: %s' % output)

        os.environ['PATH'] = original_path

        return status, output

    def _get_output_path(self, in_path, out_dir, executable, working_dir):
        base_name = os.path.splitext(os.path.split(in_path)[1])[0]
        file_name = base_name + self.extensions[executable]
        if out_dir is None:
            # use config to deduce output file path.
            out_dir = self.config['output-directory']
            if not os.path.isabs(out_dir):
                out_dir = os.path.abspath(
                    os.path.join(os.path.dirname(in_path), out_dir))
            # use the same base name but change extension
            abs_out_path = os.path.normpath(os.path.join(out_dir, file_name))
        else:
            abs_out_path = os.path.normpath(os.path.join(
                out_dir, file_name))
            if not os.path.isabs(abs_out_path):
                abs_out_path = os.path.join(working_dir, abs_out_path)
        rel_out_path = os.path.relpath(abs_out_path, working_dir)
        if ' ' in rel_out_path:
            rel_out_path = '"%s"' % rel_out_path
        return abs_out_path, rel_out_path

    def _make_cobc_command(self, in_filename, out_path, executable):
        cfg = self.config
        pgm = cfg['cobc']
        args = []
        # executable flag
        if executable:
            args.append('-x')
        # output path
        args.append('-o')
        args.append(out_path)
        # standard
        if cfg['standard'].lower() != 'none':
            args.append('-std=%s' % cfg['standard'])
        # free format
        if cfg['free-format']:
            args.append('--free')
        # compiler flags
        if cfg['-static']:
            args.append('-static')
        if cfg['-debug']:
            args.append('-debug')
        if cfg['-g']:
            args.append('-g')
        if cfg['-ftrace']:
            args.append('-ftrace')
        if cfg['-ftraceall']:
            args.append('-ftraceall')
        if cfg['-fdebugging-line']:
            args.append('-fdebugging-line')
        # extra compiler flags
        args += cfg['extra-compiler-flags']
        # copybook paths
        args += ['-I%s' % pth for pth in cfg['copybook-paths']]
        # library paths
        args += ['-L%s' % pth for pth in cfg['library-paths']]
        # libraries
        args += ['-l%s' % pth for pth in cfg['libraries']]
        args.append(in_filename)
        if 'additional-flags' in cfg.keys():
            args += cfg['additional-flags']

        return os.path.normpath(pgm), args

    @staticmethod
    def parse_output(output, working_directory, use_dicts=False):
        """
        Parses the compiler output.

        :param output: to parse
        :type output: str

        :param working_directory: the working directory where the compiler
            command was executed. This helps resolve path to relative
            copybooks.
        :type working_directory: str
        """
        issues = []
        for line in output.splitlines():
            if not line:
                continue
            for ptrn in GnuCOBOLCompiler.OUTPUT_PATTERNS:
                m = ptrn.match(line)
                if m is not None:
                    filename = m.group('filename')
                    line = int(m.group('line')) - 1
                    message = m.group('msg')
                    level = m.group('level')
                    if 'warning' in level.lower():
                        level = CheckerMessages.WARNING
                    else:
                        level = CheckerMessages.ERROR

                    # make relative path absolute
                    path = os.path.abspath(os.path.join(
                        working_directory, filename))
                    if use_dicts:
                        msg = (message, level, int(line),
                               0, None, None, path)
                    else:
                        msg = CheckerMessage(
                            message, level, int(line),
                            path=path)
                    issues.append(msg)
                    break
        return issues


def _logger():
    return logging.getLogger(__name__)


def check_mtime(in_path, abs_out_path):
    try:
        return os.path.getmtime(in_path) > os.path.getmtime(abs_out_path)
    except OSError:
        return True
