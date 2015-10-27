import glob
import hashlib
import imp
import inspect
import itertools
import math
import optparse
import os
import platform
import re
import socket
import subprocess
import sys
import tempfile
import time
import traceback
import uuid

import logging
log = logging.getLogger(__name__)


# Tornado
try:
    from tornado import ioloop
    from tornado import version_info as tornado_version
except ImportError:
    # We are likely running the agent without the forwarder and tornado is not installed
    # Generate a warning
    log.warn('Tornado web server is not installed.  Metrics will not be forwarded to the Monasca API!')

VALID_HOSTNAME_RFC_1123_PATTERN = re.compile(
    r"^(([a-zA-Z0-9]|[a-zA-Z0-9][a-zA-Z0-9\-]*[a-zA-Z0-9])\.)*([A-Za-z0-9]|[A-Za-z0-9][A-Za-z0-9\-]*[A-Za-z0-9])$")
MAX_HOSTNAME_LEN = 255
LOGGING_MAX_BYTES = 5 * 1024 * 1024

NumericTypes = (float, int, long)

import monasca_agent.common.config as configuration
from monasca_agent.common.exceptions import PathNotFound


class PidFile(object):
    """A small helper class for pidfiles. """

    PID_DIR = '/var/run/monasca-agent'

    def __init__(self, program, pid_dir=None):
        self.pid_file = "%s.pid" % program
        self.pid_dir = pid_dir or self.get_default_pid_dir()
        self.pid_path = os.path.join(self.pid_dir, self.pid_file)

    @staticmethod
    def get_default_pid_dir():
        if get_os() != 'windows':
            return PidFile.PID_DIR

        return tempfile.gettempdir()

    def get_path(self):
        # Can we write to the directory
        try:
            if os.access(self.pid_dir, os.W_OK):
                log.info("Pid file is: %s" % self.pid_path)
                return self.pid_path
        except Exception:
            log.warn("Cannot locate pid file, trying to use: %s" % tempfile.gettempdir())

        # if all else fails
        if os.access(tempfile.gettempdir(), os.W_OK):
            tmp_path = os.path.join(tempfile.gettempdir(), self.pid_file)
            log.debug("Using temporary pid file: %s" % tmp_path)
            return tmp_path
        else:
            # Can't save pid file, bail out
            log.error("Cannot save pid file anywhere")
            raise Exception("Cannot save pid file anywhere")

    def clean(self):
        try:
            path = self.get_path()
            log.debug("Cleaning up pid file %s" % path)
            os.remove(path)
            return True
        except Exception:
            log.warn("Could not clean up pid file")
            return False

    def get_pid(self):
        "Retrieve the actual pid"
        try:
            pf = open(self.get_path())
            pid_s = pf.read()
            pf.close()

            return int(pid_s.strip())
        except Exception:
            return None


class LaconicFilter(logging.Filter):
    """Filters messages, only print them once while keeping memory under control
    """
    LACONIC_MEM_LIMIT = 1024

    def __init__(self, name=""):
        logging.Filter.__init__(self, name)
        self.hashed_messages = {}

    @staticmethod
    def hash(msg):
        return hashlib.md5(msg).hexdigest()

    def filter(self, record):
        try:
            h = self.hash(record.getMessage())
            if h in self.hashed_messages:
                return 0
            else:
                # Don't blow up our memory
                if len(self.hashed_messages) >= LaconicFilter.LACONIC_MEM_LIMIT:
                    self.hashed_messages.clear()
                self.hashed_messages[h] = True
                return 1
        except Exception:
            return 1


class Timer(object):
    """Helper class """

    def __init__(self):
        self.start()

    @staticmethod
    def _now():
        return time.time()

    def start(self):
        self.started = self._now()
        self.last = self.started
        return self

    def step(self):
        now = self._now()
        step = now - self.last
        self.last = now
        return step

    def total(self, as_sec=True):
        return self._now() - self.started


class Platform(object):
    """Return information about the given platform.
    """
    @staticmethod
    def is_darwin(name=None):
        name = name or sys.platform
        return 'darwin' in name

    @staticmethod
    def is_freebsd(name=None):
        name = name or sys.platform
        return name.startswith("freebsd")

    @staticmethod
    def is_linux(name=None):
        name = name or sys.platform
        return 'linux' in name

    @staticmethod
    def is_bsd(name=None):
        """Return true if this is a BSD like operating system. """
        name = name or sys.platform
        return Platform.is_darwin(name) or Platform.is_freebsd(name)

    @staticmethod
    def is_solaris(name=None):
        name = name or sys.platform
        return name == "sunos5"

    @staticmethod
    def is_unix(name=None):
        """Return true if the platform is a unix, False otherwise. """
        name = name or sys.platform
        return (Platform.is_darwin()
                or Platform.is_linux()
                or Platform.is_freebsd()
                )

    @staticmethod
    def is_win32(name=None):
        name = name or sys.platform
        return name == "win32"


class Dimensions(object):
    """Class to update the default dimensions.
    """

    def __init__(self, agent_config):
        self.agent_config = agent_config

    def _set_dimensions(self, dimensions, instance=None):
        """Method to append the default dimensions and per instance dimensions from the config files.
        """
        new_dimensions = {'hostname': get_hostname()}

        if dimensions is not None:
            # Add or update any dimensions from the plugin itself
            new_dimensions.update(dimensions.copy())
        default_dimensions = self.agent_config.get('dimensions', {})
        if default_dimensions:
            # Add or update any default dimensions that were set in the agent config file
            new_dimensions.update(default_dimensions)
        if instance:
            # Add or update any per instance dimensions that were set in the plugin config file
            new_dimensions.update(instance.get('dimensions', {}))
        return new_dimensions


class Paths(object):
    """Return information about system paths.
    """
    def __init__(self):
        self.osname = get_os()

    def get_confd_path(self):
        bad_path = ''
        if self.osname == 'windows':
            try:
                return self._windows_confd_path()
            except PathNotFound as e:
                if len(e.args) > 0:
                    bad_path = e.args[0]
        else:
            try:
                return self._unix_confd_path()
            except PathNotFound as e:
                if len(e.args) > 0:
                    bad_path = e.args[0]

        cur_path = os.path.dirname(os.path.realpath(__file__))
        cur_path = os.path.join(cur_path, 'conf.d')

        if os.path.exists(cur_path):
            return cur_path

        raise PathNotFound(bad_path)

    def _unix_confd_path(self):
        path = os.path.join(os.path.dirname(configuration.DEFAULT_CONFIG_FILE), 'conf.d')
        path2 = os.path.join(os.getcwd(), 'conf.d')
        if os.path.exists(path):
            return path
        elif os.path.exists(path2):
            return path2
        raise PathNotFound(path)

    def _windows_confd_path(self):
        common_data = self._windows_commondata_path()
        path = os.path.join(common_data, 'Datadog', 'conf.d')
        if os.path.exists(path):
            return path
        raise PathNotFound(path)

    def get_checksd_path(self):
        if self.osname == 'windows':
            return self._windows_checksd_path()
        else:
            return self._unix_checksd_path()

    def _unix_checksd_path(self):
        # Unix only will look up based on the current directory
        # because checks_d will hang with the other python modules
        cur_path = os.path.dirname(os.path.realpath(__file__))
        checksd_path = os.path.join(cur_path, '../collector/checks_d')

        if os.path.exists(checksd_path):
            return checksd_path
        raise PathNotFound(checksd_path)

    def _windows_checksd_path(self):
        if hasattr(sys, 'frozen'):
            # we're frozen - from py2exe
            prog_path = os.path.dirname(sys.executable)
            checksd_path = os.path.join(prog_path, '..', 'checks_d')
        else:
            cur_path = os.path.dirname(__file__)
            checksd_path = os.path.join(cur_path, '../collector/checks_d')

        if os.path.exists(checksd_path):
            return checksd_path
        raise PathNotFound(checksd_path)

    def _windows_commondata_path():
        """Return the common appdata path, using ctypes
        From http://stackoverflow.com/questions/626796/\
        how-do-i-find-the-windows-common-application-data-folder-using-python
        """
        import ctypes
        from ctypes import windll
        from ctypes import wintypes

        _SHGetFolderPath = windll.shell32.SHGetFolderPathW
        _SHGetFolderPath.argtypes = [wintypes.HWND,
                                     ctypes.c_int,
                                     wintypes.HANDLE,
                                     wintypes.DWORD, wintypes.LPCWSTR]

        path_buf = wintypes.create_unicode_buffer(wintypes.MAX_PATH)
        return path_buf.value

    def set_win32_cert_path(self):
        """In order to use tornado.httpclient with the packaged .exe on Windows we
        need to override the default ceritifcate location which is based on the path
        to tornado and will give something like "C:\path\to\program.exe\tornado/cert-file".
        """
        if hasattr(sys, 'frozen'):
            # we're frozen - from py2exe
            prog_path = os.path.dirname(sys.executable)
            crt_path = os.path.join(prog_path, 'ca-certificates.crt')
        else:
            cur_path = os.path.dirname(__file__)
            crt_path = os.path.join(cur_path, 'packaging', 'monasca-agent', 'win32',
                                    'install_files', 'ca-certificates.crt')
        import tornado.simple_httpclient
        log.info("Windows certificate path: %s" % crt_path)
        tornado.simple_httpclient._DEFAULT_CA_CERTS = crt_path


def plural(count):
    if count == 1:
        return ""
    return "s"


def get_tornado_ioloop():
    if tornado_version[0] == 3:
        return ioloop.IOLoop.current()
    else:
        return ioloop.IOLoop.instance()


def get_uuid():
    # Generate a unique name that will stay constant between
    # invocations, such as platform.node() + uuid.getnode()
    # Use uuid5, which does not depend on the clock and is
    # recommended over uuid3.
    # This is important to be able to identify a server even if
    # its drives have been wiped clean.
    # Note that this is not foolproof but we can reconcile servers
    # on the back-end if need be, based on mac addresses.
    return uuid.uuid5(uuid.NAMESPACE_DNS, platform.node() + str(uuid.getnode())).hex


def get_os():
    "Human-friendly OS name"
    if sys.platform == 'darwin':
        return 'mac'
    elif sys.platform.find('freebsd') != -1:
        return 'freebsd'
    elif sys.platform.find('linux') != -1:
        return 'linux'
    elif sys.platform.find('win32') != -1:
        return 'windows'
    elif sys.platform.find('sunos') != -1:
        return 'solaris'
    else:
        return sys.platform


def headers(agentConfig):
    # Build the request headers
    return {
        'User-Agent': 'Mon Agent/%s' % agentConfig['version'],
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'text/html, */*',
    }


def getTopIndex():
    macV = None
    if sys.platform == 'darwin':
        macV = platform.mac_ver()

    # Output from top is slightly modified on OS X 10.6 (case #28239)
    if macV and macV[0].startswith('10.6.'):
        return 6
    else:
        return 5


def isnan(val):
    if hasattr(math, 'isnan'):
        return math.isnan(val)

    # for py < 2.6, use a different check
    # http://stackoverflow.com/questions/944700/how-to-check-for-nan-in-python
    return str(val) == str(1e400 * 0)


def cast_metric_val(val):
    # ensure that the metric value is a numeric type
    if not isinstance(val, NumericTypes):
        # Try the int conversion first because want to preserve
        # whether the value is an int or a float. If neither work,
        # raise a ValueError to be handled elsewhere
        for cast in [int, float]:
            try:
                val = cast(val)
                return val
            except ValueError:
                continue
        raise ValueError
    return val


def is_valid_hostname(hostname):
    if hostname.lower() in ('localhost', 'localhost.localdomain',
                            'localhost6.localdomain6', 'ip6-localhost'):
        log.warning("Hostname: %s is local" % hostname)
        return False
    if len(hostname) > MAX_HOSTNAME_LEN:
        log.warning("Hostname: %s is too long (max length is  %s characters)" %
                    (hostname, MAX_HOSTNAME_LEN))
        return False
    if VALID_HOSTNAME_RFC_1123_PATTERN.match(hostname) is None:
        log.warning("Hostname: %s is not complying with RFC 1123" % hostname)
        return False
    return True


def get_hostname():
    """Get the canonical host name this agent should identify as. This is
       the authoritative source of the host name for the agent.

    Tries, in order:

      * agent config (agent.yaml, "hostname:")
      * 'hostname -f' (on unix)
      * socket.gethostname()
    """
    hostname = None

    # first, try the config
    config = configuration.Config()
    agent_config = config.get_config(sections='Main')
    config_hostname = agent_config.get('hostname')
    if config_hostname and is_valid_hostname(config_hostname):
        return config_hostname

    # then move on to os-specific detection
    if hostname is None:
        def _get_hostname_unix():
            try:
                # try fqdn
                p = subprocess.Popen(['/bin/hostname', '-f'], stdout=subprocess.PIPE)
                out, err = p.communicate()
                if p.returncode == 0:
                    return out.strip()
            except Exception:
                return None

        os_name = get_os()
        if os_name in ['mac', 'freebsd', 'linux', 'solaris']:
            unix_hostname = _get_hostname_unix()
            if unix_hostname and is_valid_hostname(unix_hostname):
                hostname = unix_hostname

    # fall back on socket.gethostname(), socket.getfqdn() is too unreliable
    if hostname is None:
        try:
            socket_hostname = socket.gethostname()
        except socket.error:
            socket_hostname = None
        if socket_hostname and is_valid_hostname(socket_hostname):
            hostname = socket_hostname

    if hostname is None:
        log.critical(
            'Unable to reliably determine host name. You can define one in agent.yaml or in your hosts file')
        raise Exception(
            'Unable to reliably determine host name. You can define one in agent.yaml or in your hosts file')
    else:
        return hostname


def get_parsed_args():
    parser = optparse.OptionParser()
    parser.add_option('-c', '--clean', action='store_true', default=False, dest='clean')
    parser.add_option('-v', '--verbose', action='store_true', default=False, dest='verbose',
                      help='Print out stacktraces for errors in checks')

    try:
        options, args = parser.parse_args()
    except SystemExit:
        # Ignore parse errors
        options, args = optparse.Values({'clean': False}), []
    return options, args


def load_check_directory():
    """Return the initialized checks from checks_d, and a mapping of checks that failed to
    initialize. Only checks that have a configuration
    file in conf.d will be returned.
    """

    from monasca_agent.collector.checks import AgentCheck

    config = configuration.Config()
    agent_config = config.get_config('Main')

    initialized_checks = {}
    init_failed_checks = {}

    paths = Paths()
    checks_paths = [glob.glob(os.path.join(agent_config['additional_checksd'], '*.py'))]

    try:
        checksd_path = paths.get_checksd_path()
        checks_paths.append(glob.glob(os.path.join(checksd_path, '*.py')))
    except PathNotFound as e:
        log.error(e.args[0])
        sys.exit(3)

    try:
        confd_path = paths.get_confd_path()
    except PathNotFound as e:
        log.error(
            "No conf.d folder found at '%s' or in the directory where the Agent is currently deployed.\n" %
            e.args[0])
        sys.exit(3)

    # For backwards-compatability with old style checks, we have to load every
    # checks_d module and check for a corresponding config OR check if the old
    # config will "activate" the check.
    #
    # Once old-style checks aren't supported, we'll just read the configs and
    # import the corresponding check module
    for check in itertools.chain(*checks_paths):
        check_name = os.path.basename(check).split('.')[0]
        if check_name in initialized_checks or check_name in init_failed_checks:
            log.debug(
                'Skipping check %s because it has already been loaded from another location', check)
            continue
        try:
            check_module = imp.load_source('checksd_%s' % check_name, check)
        except Exception as e:
            traceback_message = traceback.format_exc()

            # Let's see if there is a conf.d for this check
            conf_path = os.path.join(confd_path, '%s.yaml' % check_name)
            if os.path.exists(conf_path):
                # There is a configuration file for that check but the module can't be imported
                init_failed_checks[check_name] = {'error': e, 'traceback': traceback_message}
                log.exception('Unable to import check module %s.py from checks_d' % check_name)
            else:  # There is no conf for that check. Let's not spam the logs for it.
                log.debug('Unable to import check module %s.py from checks_d' % check_name)
            continue

        check_class = None
        classes = inspect.getmembers(check_module, inspect.isclass)
        for _, clsmember in classes:
            if clsmember == AgentCheck:
                continue
            if issubclass(clsmember, AgentCheck):
                check_class = clsmember
                if AgentCheck in clsmember.__bases__:
                    continue
                else:
                    break

        if not check_class:
            if not check_name == '__init__':
                log.error('No check class (inheriting from AgentCheck) found in %s.py' % check_name)
                continue

        # Check if the config exists
        conf_path = os.path.join(confd_path, '%s.yaml' % check_name)
        if os.path.exists(conf_path):
            try:
                check_config = config.check_yaml(conf_path)
            except Exception as e:
                log.exception("Unable to parse yaml config in %s" % conf_path)
                traceback_message = traceback.format_exc()
                init_failed_checks[check_name] = {'error': e, 'traceback': traceback_message}
                continue
        else:
            log.debug('No conf.d/%s.yaml found for checks_d/%s.py' % (check_name, check_name))
            continue

        # Look for the per-check config, which *must* exist
        if not check_config.get('instances'):
            log.error("Config %s is missing 'instances'" % conf_path)
            continue

        # Init all of the check's classes with
        init_config = check_config.get('init_config', {})
        # init_config: in the configuration triggers init_config to be defined
        # to None.
        if init_config is None:
            init_config = {}

        instances = check_config['instances']
        try:
            try:
                c = check_class(check_name, init_config=init_config,
                                agent_config=agent_config, instances=instances)
            except TypeError as e:
                # Backwards compatibility for checks which don't support the
                # instances argument in the constructor.
                c = check_class(check_name, init_config=init_config,
                                agent_config=agent_config)
                c.instances = instances
        except Exception as e:
            log.exception('Unable to initialize check %s' % check_name)
            traceback_message = traceback.format_exc()
            init_failed_checks[check_name] = {'error': e, 'traceback': traceback_message}
        else:
            initialized_checks[check_name] = c

        # Add custom pythonpath(s) if available
        if 'pythonpath' in check_config:
            pythonpath = check_config['pythonpath']
            if not isinstance(pythonpath, list):
                pythonpath = [pythonpath]
            sys.path.extend(pythonpath)

        log.debug('Loaded check.d/%s.py' % check_name)

    log.info('Successfully initialized checks: %s' % initialized_checks.keys())
    if len(init_failed_checks) > 0:
        log.info('Initialization failed for checks: %s' % init_failed_checks.keys())
    return {'initialized_checks': initialized_checks.values(),
            'init_failed_checks': init_failed_checks,
            }


def initialize_logging(logger_name):
    try:
        log_format = '%%(asctime)s | %%(levelname)s | %s | %%(name)s(%%(filename)s:%%(lineno)s) | %%(message)s' % logger_name
        log_date_format = "%Y-%m-%d %H:%M:%S %Z"
        config = configuration.Config()
        logging_config = config.get_config(sections='Logging')

        logging.basicConfig(
            format=log_format,
            level=logging_config['log_level'] or logging.INFO,
        )

        # set up file loggers
        log_file = logging_config.get('%s_log_file' % logger_name)
        if log_file is not None and not logging_config['disable_file_logging']:
            # make sure the log directory is writeable
            # NOTE: the entire directory needs to be writable so that rotation works
            if os.access(os.path.dirname(log_file), os.R_OK | os.W_OK):
                file_handler = logging.handlers.RotatingFileHandler(
                    log_file, maxBytes=LOGGING_MAX_BYTES, backupCount=1)
                formatter = logging.Formatter(log_format, log_date_format)
                file_handler.setFormatter(formatter)

                root_log = logging.getLogger()
                root_log.addHandler(file_handler)
            else:
                sys.stderr.write("Log file is unwritable: '%s'\n" % log_file)

        # set up syslog
        if logging_config['log_to_syslog']:
            try:
                syslog_format = '%s[%%(process)d]: %%(levelname)s (%%(filename)s:%%(lineno)s): %%(message)s' % logger_name
                from logging.handlers import SysLogHandler

                if logging_config['syslog_host'] is not None and logging_config[
                        'syslog_port'] is not None:
                    sys_log_addr = (logging_config['syslog_host'], logging_config['syslog_port'])
                else:
                    sys_log_addr = "/dev/log"
                    # Special-case macs
                    if sys.platform == 'darwin':
                        sys_log_addr = "/var/run/syslog"

                handler = SysLogHandler(address=sys_log_addr, facility=SysLogHandler.LOG_DAEMON)
                handler.setFormatter(
                    logging.Formatter(syslog_format, log_date_format))
                root_log = logging.getLogger()
                root_log.addHandler(handler)
            except Exception as e:
                sys.stderr.write("Error setting up syslog: '%s'\n" % str(e))
                traceback.print_exc()

    except Exception as e:
        sys.stderr.write("Couldn't initialize logging: %s\n" % str(e))
        traceback.print_exc()

        # if config fails entirely, enable basic stdout logging as a fallback
        logging.basicConfig(
            format=log_format,
            level=logging.INFO,
        )

    # re-get the log after logging is initialized
    global log
    log = logging.getLogger(__name__)


"""
Iterable Recipes
"""


def chunks(iterable, chunk_size):
    """Generate sequences of `chunk_size` elements from `iterable`."""
    iterable = iter(iterable)
    while True:
        chunk = [None] * chunk_size
        count = 0
        try:
            for _ in range(chunk_size):
                chunk[count] = iterable.next()
                count += 1
            yield chunk[:count]
        except StopIteration:
            if count:
                yield chunk[:count]
            break
