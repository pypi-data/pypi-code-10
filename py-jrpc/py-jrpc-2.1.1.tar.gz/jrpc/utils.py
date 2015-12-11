import os
import sys

from Crypto.PublicKey import RSA

__author__ = 'umairghani'

ansi = {
    'red':      '\033[0;31m',
    'yellow':   '\033[0;33m',
    'blue':     '\033[0;34m',
    'magenta':  '\033[0;35m',
    'reset':    '\033[0m',
    }

def deamonize(name):
    """
    Function to deamonize the process
    :param name
    """
    if os.fork() > 0: sys.exit(0)
    os.setsid()
    if os.fork() > 0: sys.exit(0)
    si = open('/dev/null', 'r')
    so = open('/dev/null', 'a+')
    se = open('/dev/null', 'a+', 0)
    os.dup2(si.fileno(), sys.stdin.fileno())
    os.dup2(so.fileno(), sys.stdout.fileno())
    os.dup2(se.fileno(), sys.stderr.fileno())
    # Writing pid file
    pid = os.getpid()
    PIDFILE = "/var/run/%s.pid" % name
    f = open(PIDFILE, 'w')
    f.write(str(pid))
    f.close()


def rsaHandShake(publicKey, privateKey):
    """
    RSA handshake function to make sure
    private and public key bind
    :param public key
    :param private key
    :return boolean True/False
    """
    key = RSA.importKey(privateKey)
    return key.publickey().exportKey('PEM') == publicKey

