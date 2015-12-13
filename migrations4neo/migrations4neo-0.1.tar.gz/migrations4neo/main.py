import binascii
import ConfigParser
import imp
import os
import argparse

from slugify import Slugify

from . import template
from . import utils


PARSER_INIT = 'init'
PARSER_REVISION = 'revision'
PARSER_UPGRADE = 'upgrade'
PARSER_DOWNGRADE = 'downgrade'

MIGRATION_PARSERS = [PARSER_UPGRADE, PARSER_DOWNGRADE]
PARSER_NAMES = [PARSER_INIT, PARSER_REVISION] + MIGRATION_PARSERS

INI_SECTION = 'mig4neo'
INI_DB_KEY = 'neo4j.db_uri'
INI_LOCATION = 'location'

CANNOT_FIND = """
!!!!!!!!!!!!!
ERROR: Cannot find revisions: {}'
!!!!!!!!!!!!!
"""

MIGRATION_INFO = """
#############
INFO: : {} DONE'
#############
"""


def init(directory):
    mig4neo_path = os.path.abspath(directory)
    revisions_path = os.path.join(mig4neo_path, 'revisions')
    ini_path = os.path.abspath('mig4neo.ini')

    for dir_path in (mig4neo_path, revisions_path):
        dir_path = os.path.join(mig4neo_path, dir_path)
        if os.path.exists(dir_path):
            msg = 'Creating directory {}...already exists'.format(dir_path)
            utils.message(msg)
        else:
            os.makedirs(dir_path)
            msg = 'Creating directory {}...created'.format(dir_path)
            utils.message(msg)

    if os.path.exists(ini_path):
        msg = 'Generating ini file {}...already exists'.format(ini_path)
        utils.message(msg)
    else:
        db_uri = 'http://user:password@localhost:7474/db/data/'
        config = ConfigParser.RawConfigParser()
        config.add_section('mig4neo')
        config.set(INI_SECTION, INI_DB_KEY, db_uri)
        config.set(INI_SECTION, INI_LOCATION, directory)

        with open(ini_path, 'wb') as ini_file:
            config.write(ini_file)
        msg = 'Generating ini file {}...created'.format(ini_path)
        utils.message(msg)


def revision(args):
    ini_path = os.path.abspath(args.config)
    config = ConfigParser.RawConfigParser()
    config.read(ini_path)
    directory = config.get(INI_SECTION, INI_LOCATION)
    mig4neo_path = os.path.abspath(directory)

    message = args.message
    mag_slugify = Slugify(to_lower=True)
    mag_slugify.separator = '_'
    message = mag_slugify(message)
    number = binascii.hexlify(os.urandom(5))
    revision_filename = '{}_{}.py'.format(number, message)
    revision_body = template.body.format(number)
    revisions_path = os.path.join(mig4neo_path, 'revisions')
    revision_path = os.path.join(revisions_path, revision_filename)
    with open(revision_path, 'wb') as revision_file:
        revision_file.write(revision_body)
    msg = 'Generating revision file {}...created'.format(revision_path)
    utils.message(msg)


def run_migrations(args, action):
    config = args.config
    revisions = args.revisions
    ini_path = os.path.abspath(args.config)
    config = ConfigParser.RawConfigParser()
    config.read(ini_path)
    directory = config.get(INI_SECTION, INI_LOCATION)
    mig4neo_path = os.path.abspath(directory)
    revisions_path = os.path.join(mig4neo_path, 'revisions')

    config = ConfigParser.RawConfigParser()
    config.read(ini_path)
    db_uri = config.get(INI_SECTION, INI_DB_KEY)
    os.environ['NEO4J_REST_URL'] = db_uri

    filenames = os.listdir(revisions_path)
    filename_numbers = {}
    for filename in filenames:
        key = filename.split('_')[0]
        filename_path = os.path.join(revisions_path, filename)
        filename_numbers[key] = filename_path
    revision_numbers = revisions.split(',')

    missing = []
    for revision_number in revision_numbers:
        if revision_number not in filename_numbers:
            missing.append(revision_number)

    if missing:
        missing = ','.join(missing)
        msg = CANNOT_FIND.format(missing)
        utils.message(msg)
        return
    filename_paths = [filename_numbers[name] for name in revision_numbers]
    for filename_path, revision in zip(filename_paths, revisions):
        module = load_module(revision, filename_path)
        getattr(module, action)()
    msg = MIGRATION_INFO.format(revisions)
    utils.message(msg)
    

def load_module(revision, path):
    with open(path, 'rb') as f:
        return imp.load_source(revision, path, f)


def upgrade(args):
    run_migrations(args, 'up')


def downgrade(args):
    run_migrations(args, 'down')


def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()

    for parser_name in PARSER_NAMES:
        _parser = subparsers.add_parser(parser_name)
        _parser.set_defaults(which=parser_name)

    #TODO: prettify needed
    subparsers.choices.get(PARSER_INIT).add_argument(
        'directory', help='Directory for migrations4neo',
        default='mig4neo'
    )
    subparsers.choices.get(PARSER_REVISION).add_argument(
        '-m', '--message', type=str, dest='message',
        help='Create new revision with message',
        default=None
    )
    subparsers.choices.get(PARSER_REVISION).add_argument(
        '-c', '--config', dest='config',
        help='Alternate config file',
        default='mig4neo.ini'
    )
    for migration_parser in MIGRATION_PARSERS:
        subparsers.choices.get(migration_parser).add_argument(
            '-r', '--revisions', dest='revisions',
            help='Upgrades with provided revisions',
            default=None
        )
        subparsers.choices.get(migration_parser).add_argument(
            '-c', '--config', dest='config',
            help='Alternate config file',
            default='mig4neo.ini'
        )

    #TODO: prettify needed
    parsed_args = parser.parse_args()
    if parsed_args.which == PARSER_INIT:
        init(parsed_args.directory)
    elif parsed_args.which == PARSER_REVISION:
        revision(parsed_args)
    elif parsed_args.which == PARSER_UPGRADE:
        upgrade(parsed_args)
    elif parsed_args.which == PARSER_DOWNGRADE:
        downgrade(parsed_args)
    else:
        msg = 'Please tell me what to do :)'
        utils.message(msg)
