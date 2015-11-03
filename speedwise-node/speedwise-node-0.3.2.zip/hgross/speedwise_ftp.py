import argparse
import codecs
import os
import sys
from hgross.ac.common import ACServerWrapperConfig

__author__ = 'Henning Gross'
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer

RETVAL_ERROR_CONFIG = -1 # on misconfiguration

def main_func():
    "The main"
    sys.stdout = codecs.getwriter("utf8")(sys.stdout);
    argParser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter, description="Starts a FTP-server on port 9056 and the configured path to the ac dedicated server's base directory as root path. Can be used with the AssettoCorsaServerManager to upload new acServer versions.")
    argParser.add_argument('--config-file', default="speedwise.ini", help='The assetto corsa wrapper\'s config file path. If not specified, speedwise.ini in the current directory will be used (must exist.')
    args = argParser.parse_args()

    # load config
    if not os.path.isfile(args.config_file):
        print (u"Config not found! Sign in to speedwise (http://speedwise.de/gameserver_admins/gameservers/) to get your shared secret and server id and follow the instructions.\n\n Use -h for help.")
        sys.exit(1)
    wrapperConfig = ACServerWrapperConfig(args.config_file)

    # validate directory existance
    if not os.path.isdir(wrapperConfig.DEDICATED_SERVER_BASE_DIRECTORY):
        print ("ERROR: the configured ac base directory path (speedwise.ini) is not valid (%s)" % wrapperConfig.DEDICATED_SERVER_BASE_DIRECTORY)
        sys.exit(RETVAL_ERROR_CONFIG)

    secret = wrapperConfig.speedwise_server_secret

    # set up and ftp server
    authorizer = DummyAuthorizer()
    ftp_dir = wrapperConfig.DEDICATED_SERVER_BASE_DIRECTORY
    authorizer.add_user("speedwise", secret, ftp_dir, perm="elradfmw")

    handler = FTPHandler
    handler.authorizer = authorizer

    server = FTPServer(("0.0.0.0", 9056), handler)
    server.serve_forever()

if __name__ == "__main__":
    main_func()