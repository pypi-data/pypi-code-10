import argparse
from credkeep.encrypt import encrypt_file


def add_encrypt_parser(subparsers):
    encrypt = subparsers.add_parser('encrypt', help='encrypt a secrets file')
    encrypt.add_argument('input', help='input filename')
    encrypt.add_argument('-o', '--out', help='Output filename')
    encrypt.add_argument('-k', '--key', help='AWS KMS key name')

def run_command(args):
    if args.cmd == 'encrypt':
        encrypt_file(args.input, key=args.key, output_filename=args.out)


def main():
    parser = argparse.ArgumentParser(prog='credkeep',
                                     description="Securely encrypted using AWS's Key Management Service (KMS)")
    subparsers = parser.add_subparsers(dest='cmd')

    add_encrypt_parser(subparsers)

    args = parser.parse_args()
    run_command(args)


if __name__ == '__init__':
    main()
