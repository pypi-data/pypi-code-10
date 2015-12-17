import argparse
from credkeep.encrypt import encrypt_file
from credkeep.decrypt import decrypt_file


def add_encrypt_parser(subparsers):
    encrypt = subparsers.add_parser('encrypt', help='encrypt a secrets file')
    encrypt.add_argument('input', help='input filename')
    encrypt.add_argument('-o', '--out', help='Output filename')
    encrypt.add_argument('-k', '--key', help='AWS KMS key name')


def add_decrypt_parser(subparsers):
    decrypt = subparsers.add_parser('decrypt', help='decrypt a file encrypted with KMS')
    decrypt.add_argument('input', help='input filename')
    decrypt.add_argument('-e', '--env', help='Set environment variable with decrypted keys', action='store_true')
    decrypt.add_argument('--override', help="Don't override existing environment variables", action='store_true',
                         default=False)

def run_command(args):
    if args.cmd == 'encrypt':
        encrypt_file(args.input, key=args.key, output_filename=args.out)
    elif args.cmd == 'decrypt':
        decrypt_file(args.input, set_env=args.env, override_env=args.override )


def main():
    parser = argparse.ArgumentParser(prog='credkeep',
                                     description="Securely encrypted using AWS's Key Management Service (KMS)")
    subparsers = parser.add_subparsers(dest='cmd')

    add_encrypt_parser(subparsers)
    add_decrypt_parser(subparsers)

    args = parser.parse_args()
    run_command(args)


if __name__ == '__init__':
    main()
