import argparse
import os
import logging
import shutil
import time
from glob import glob

from .microbit_path import get_default_microbit_path


logger = logging.getLogger(__name__)

HEX_GLOB = 'micropython*.hex'
SLEEP_TIME = 1

class ParamError(ValueError):
    pass

def get_default_download_path():
    home = os.path.expanduser('~')
    return os.path.join(home, 'Downloads')


def reflash_upon_new(download_path, microbit_path):
    if not microbit_path:
        raise ParamError("Need to set microbit_path")
    if not os.path.exists(download_path):
        raise ParamError("download_path {} doesn't exist".format(download_path))
    if not os.path.isdir(download_path):
        raise ParamError("download_path {} isn't a directory".format(download_path))

    previous_hex = None
    while True:
        all_hexes = glob(os.path.join(download_path, HEX_GLOB))
        latest_hex_path = max(all_hexes, key=os.path.getctime)
        if latest_hex_path != previous_hex:
            logger.info(latest_hex_path)
            shutil.copy(latest_hex_path, microbit_path)
        time.sleep(SLEEP_TIME)
        previous_hex = latest_hex_path


def main():
    parser = argparse.ArgumentParser(
        description='A command to watch for new hex files from '
        'https://github.com/ntoll/upyed and flash the micro:bit immediately')

    parser.add_argument(
        '--download_path',
        type=str,
        default=get_default_download_path(),
        help='Filepath your browser stores downloads'
    )

    parser.add_argument(
        '--microbit_path',
        type=str,
        default=get_default_microbit_path(),
        help='Filepath your computer mounts the Micro:bit at'
    )

    parser.add_argument(
        '-v',
        '--verbose',
        action='store_true',
        default=False,
    )

    args = parser.parse_args()

    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)
        logger.debug(args)

    reflash_upon_new(args.download_path, args.microbit_path)


if __name__ == '__main__':
    main()
