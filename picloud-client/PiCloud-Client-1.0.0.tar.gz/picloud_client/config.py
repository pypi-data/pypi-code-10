import os


def getenv_required(key):
    v = os.getenv(key)
    if v is None:
        raise ValueError("{0} environment variable is not exported".format(key))
    return v


PICLOUD_URL = getenv_required('PICLOUD_URL')
PICLOUD_API_KEY = getenv_required('PICLOUD_API_KEY')
