import argparse

import pi
import slice


def main():
    roles = {
        'client': slice.main,
        'server': pi.main,
    }

    parser = argparse.ArgumentParser(description='''
        Create a server and clients to establish a Bluetooth network that
        monitors the light sensors of each client.
    ''')

    parser.add_argument('role',
                        help='''choose the role of the system''',
                        choices=roles.keys())

    args = parser.parse_args()

    roles[args.role]()


if __name__ == '__main__':
    main()

from ._version import get_versions
__version__ = get_versions()['version']
del get_versions
