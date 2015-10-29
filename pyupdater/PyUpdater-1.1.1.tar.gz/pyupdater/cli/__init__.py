# --------------------------------------------------------------------------
# Copyright 2014 Digital Sapphire Development Team
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# --------------------------------------------------------------------------
from __future__ import unicode_literals

import json
import logging
import os
import sys
import warnings

from appdirs import user_log_dir
from jms_utils.logger import log_formatter
from jms_utils.paths import ChDir
from jms_utils.terminal import ask_yes_no, get_correct_answer
import requests
import stevedore


from pyupdater import PyUpdater, __version__
from pyupdater import settings
from pyupdater.builder import Builder, ExternalLib
from pyupdater.cli.options import get_parser
from pyupdater.key_handler.keys import Keys, KeyImporter
from pyupdater.utils import (check_repo,
                             initial_setup,
                             remove_any,
                             setup_company,
                             setup_urls,
                             setup_patches,
                             setup_scp,
                             setup_object_bucket)
from pyupdater.utils.config import ConfigDict, Loader
from pyupdater.utils.exceptions import UploaderError, UploaderPluginError


CWD = os.getcwd()
log = logging.getLogger()
if os.path.exists(os.path.join(CWD, 'pyu.log')):  # pragma: no cover
    fh = logging.FileHandler(os.path.join(CWD, 'pyu.log'))
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(log_formatter())
    log.addHandler(fh)

fmt = logging.Formatter('[%(levelname)s] %(message)s')
sh = logging.StreamHandler()
sh.setFormatter(fmt)

sh.setLevel(logging.INFO)
# Used for Development
# sh.setLevel(logging.DEBUG)
log.addHandler(sh)

# We'll only keep one backup log file
LOG_DIR = user_log_dir(settings.APP_NAME, settings.APP_AUTHOR)
log_file = os.path.join(LOG_DIR, settings.LOG_FILENAME_DEBUG)
rfh = logging.handlers.RotatingFileHandler(log_file, maxBytes=9445269,
                                           backupCount=2)
rfh.setFormatter(log_formatter())
rfh.setLevel(logging.DEBUG)
log.addHandler(rfh)


def _repo_error():
    log.error('Not a PyUpdater repo: You must initialize '
              'your repository first')
    sys.exit(1)


def archive(args):
    check = check_repo()
    if check is False:
        _repo_error()
    new_dir = os.path.join(os.getcwd(), settings.USER_DATA_FOLDER, 'new')
    name = args.name
    target_name = args.target_name
    version = args.version

    with ChDir(new_dir):
        if not os.path.exists(target_name):
            log.error('{} does not exists'.format(target_name))
            return
        ex_lib = ExternalLib(name, target_name, version)
        ex_lib.archive()
        if args.keep is False:
            remove_any(target_name)
            log.info('Removed: {}'.format(target_name))


# Will build and archive an exe from a python script file
def _build(args, pyi_args):
    check = check_repo()
    if check is False:
        _repo_error()

    builder = Builder(args, pyi_args)
    builder.build()


# Get permission before deleting PyUpdater repo
def clean(args):  # pragma: no cover
    if args.yes is True:
        _clean()

    else:
        answer = ask_yes_no('Are you sure you want to remove '
                            'pyupdater data?', default='no')
        if answer is True:
            _clean()
        else:
            log.info('Clean aborted!')


# Remove all traces of PyUpdater
def _clean():
    cleaned = False
    if os.path.exists(settings.CONFIG_DATA_FOLDER):
        cleaned = True
        remove_any(settings.CONFIG_DATA_FOLDER)
        log.info('Removed {} folder'.format(settings.CONFIG_DATA_FOLDER))
    if os.path.exists(settings.USER_DATA_FOLDER):
        cleaned = True
        remove_any(settings.USER_DATA_FOLDER)
        log.info('Removed {} folder'.format(settings.USER_DATA_FOLDER))
    if cleaned is True:
        log.info('Clean complete...')
    else:
        log.info('Nothing to clean...')


# Initialize PyUpdater repo
def init(args):  # pragma: no cover
    if not os.path.exists(os.path.join(settings.CONFIG_DATA_FOLDER,
                          settings.CONFIG_FILE_USER)):
        config = ConfigDict()
        config = initial_setup(config)
        log.info('Creating pyu-data dir...')
        pyu = PyUpdater(config)
        pyu.setup()
        loader = Loader()
        loader.save_config(config)
        log.info('Setup complete')
    else:
        sys.exit('Not an empty PyUpdater repository')


def keys(args):  # pragma: no cover
    if args.yes is True:
        _keys(args)

    else:
        answer = ask_yes_no('Are you sure you want to continue?',
                            default='no')
        if answer is True:
            _keys(args)
        else:
            log.info('Command aborted!')


# Revokes keys
def _keys(args):  # pragma: no cover
    check = check_repo()
    if args.create is True and args.import_keys is True:
        log.error('Only one options is allowed at a time')
        sys.exit(1)

    if args.create is True and check is True:
        log.error('You can not create off-line keys on your dev machine')
        sys.exit(1)

    if args.import_keys is True and check is False:
        _repo_error()

    if args.create is True and check is False:
        k = Keys()
        app_name = get_correct_answer('Please enter app name',
                                      required=True)
        k.make_keypack(app_name)
        log.info('Keypack placed in cwd')
        return

    if args.import_keys is True and check is True:
        loader = Loader()
        config = loader.load_config()
        ki = KeyImporter()
        imported = ki.start()
        if imported is True:
            log.info('Keypack import successfully')
            loader.save_config(config)
        else:
            log.warning('Keypack import failed')


def _make_spec(args, pyi_args):
    check = check_repo()
    if check is False:
        _repo_error()

    builder = Builder(args, pyi_args)
    builder.make_spec()


def pkg(args):
    check = check_repo()
    if check is False:
        _repo_error()

    loader = Loader()
    pyu = PyUpdater(loader.load_config())
    if args.process is False and args.sign is False:
        sys.exit('You must specify a command')

    if args.process is True:
        log.info('Processing packages...')
        pyu.process_packages()
        log.info('Processing packages complete')
    if args.sign is True:
        log.info('Signing packages...')
        pyu.sign_update()
        log.info('Signing packages complete')


def _setting(args):  # pragma: no cover
    check = check_repo()
    if check is False:
        _repo_error()

    loader = Loader()
    config = loader.load_config()
    if args.company is True:
        setup_company(config)
    if args.urls is True:
        setup_urls(config)
    if args.patches is True:
        setup_patches(config)
    if args.scp is True:
        setup_scp(config)
    if args.s3 is True:
        setup_object_bucket(config)
    loader.save_config(config)
    log.info('Settings update complete')


def upload_debug_info(args):  # pragma: no cover
    log.info('Starting log export')

    def _add_file(payload, filename):
        with open(filename, 'r') as f:
            data = f.read()
        payload['files'][filename] = {'content': data}

    def _upload(data):
        api = 'https://api.github.com/'
        gist_url = api + 'gists'
        headers = {"Accept": "application/vnd.github.v3+json"}
        r = requests.post(gist_url, headers=headers, data=json.dumps(data))
        try:
            url = r.json()['html_url']
        except Exception as err:
            log.debug(err, exc_info=True)
            log.debug(json.dumps(r.json(), indent=2))
            url = None
        return url

    upload_data = {'files': {}}
    with ChDir(LOG_DIR):
        temp_files = os.listdir(os.getcwd())
        if len(temp_files) == 0:
            log.info('No log files to collect')
            return
        log.info('Collecting logs')
        for t in temp_files:
            if t.startswith(settings.LOG_FILENAME_DEBUG):
                log.debug('Adding {} to log'.format(t))
                _add_file(upload_data, t)
        log.info('Found all logs')
        url = _upload(upload_data)
    if url is None:
        log.error('Could not upload debug info to github')
    else:
        log.info('Log export complete')
        log.info('Logs uploaded to {}'.fomrat(url))


def upload(args):  # pragma: no cover
    check = check_repo()
    if check is False:
        _repo_error()

    error = False
    loader = Loader()
    upload_service = args.service
    if upload_service is None:
        log.error('Must provide service name')
        error = True

    if error is False:
        pyu = PyUpdater(loader.load_config())
        try:
            pyu.set_uploader(upload_service)
        except UploaderError as err:
            log.error(err)
            error = True
        except UploaderPluginError as err:
            log.debug(err)
            error = True
            mgr = stevedore.ExtensionManager(settings.UPLOAD_PLUGIN_NAMESPACE)
            plugin_names = mgr.names()
            log.debug('Plugin names: {}'.format(plugin_names))
            if len(plugin_names) == 0:
                msg = ('*** No upload plugins instaled! ***\nYou can install '
                       'the aws s3 plugin with\n$ pip install PyUpdater'
                       '[s3]\n\nOr the scp plugin with\n$ pip install '
                       'PyUpdater[scp]')
            else:
                msg = ('Invalid Uploader\n\nAvailable options:\n'
                       '{}'.format(' '.join(plugin_names)))
            log.error(msg)
    if error is False:
        try:
            pyu.upload()
        except Exception as e:
            msg = ('Looks like you forgot to add USERNAME '
                   'and/or REMOTE_DIR')
            log.debug(e, exc_info=True)
            log.error(msg)


def _real_main(args):  # pragma: no cover
    if args is None:
        args = sys.argv[1:]
    parser = get_parser()
    args, pyi_args = parser.parse_known_args(args)
    cmd = args.command
    if cmd == 'archive':
        archive(args)
    elif cmd == 'build':
        _build(args, pyi_args)
    elif cmd == 'clean':
        clean(args)
    elif cmd == 'init':
        init(args)
    elif cmd == 'keys':
        keys(args)
    # ToDo: Remove in v1.0
    elif cmd == 'log':
        warnings.simplefilter('always', DeprecationWarning)
        warnings.warn('Use "collect-debug-info" ', DeprecationWarning)
        upload_debug_info(args)
    # End to do
    elif cmd == 'collect-debug-info':
        upload_debug_info(args)
    elif cmd == 'make-spec':
        _make_spec(args, pyi_args)
    elif cmd == 'pkg':
        pkg(args)
    elif cmd == 'settings':
        _setting(args)
    elif cmd == 'update':
        update(args)
    elif cmd == 'upload':
        upload(args)
    elif cmd == 'version':
        print('PyUpdater {}'.format(__version__))
    else:
        log.error('Not Implemented')
        sys.exit(1)


def main(args=None):  # pragma: no cover
    try:
        _real_main(args)
    except KeyboardInterrupt:
        print('\n')
        msg = 'Exited by user'
        log.warning(msg)
    except Exception as err:
        log.debug(err, exc_info=True)
        log.error(err)

if __name__ == '__main__':  # pragma: no cover
    args = sys.argv[1:]
    main(args)
