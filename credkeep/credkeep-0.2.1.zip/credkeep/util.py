import boto3
from os.path import exists

kms = boto3.client('kms')
default_keyname = 'alias/credkeep'


class CredkeepException(Exception):
    pass


def clear_to_enc_filename(fname):
    """
    Converts the filename of a cleartext file and convert it to an encrypted filename

    :param fname:
    :return: filename of encrypted secret file if found, else None
    """
    if not fname.lower().endswith('.json'):
        raise CredkeepException('Invalid filetype')

    if fname.lower().endswith('.enc.json'):
        raise CredkeepException('File already encrypted')

    enc_fname = fname[:-4] + 'enc.json'

    return enc_fname if exists(enc_fname) else None


def enc_to_clear_filename(fname):
    """
    Converts the filename of an encrypted file to cleartext

    :param fname:
    :return: filename of clear secret file if found, else None
    """
    if not fname.lower().endswith('.json'):
        raise CredkeepException('Invalid filetype')

    if not fname.lower().endswith('.enc.json'):
        raise CredkeepException('Not filename of encrypted file')

    clear_fname = fname.replace('.enc.json', '.json')
    print clear_fname

    return clear_fname if exists(clear_fname) else None
