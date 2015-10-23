#! /usr/bin/env python
"""Mirage Command Line Client.
Usage:
  mclient.py login <mirage_uri>
  mclient.py new <scenario_name>
  mclient.py begin --scenario=<scenario_name> --session=<session_name> --mode=<record|playback>
  mclient.py end --scenario=<scenario_name> [--session=<session_name>]
  mclient.py remove --scenario=<scenario_name> --force=<true|false>
  mclient.py upload <file_name> [--session=<session_name>] [--scenario=<scenario_name>]
  mclient.py -h | --help
  mclient.py --version

Examples:
  mclient.py login http://boot2docker_ip:8001
  mclient.py new scenario_x

Options:
  -h --help     Show this screen.
  --version     Show version.
"""
from docopt import docopt
import requests
import os
import zipfile
import yaml
import contextlib
import shutil
from cStringIO import StringIO
from tempfile import mkdtemp


version = 0.1


@contextlib.contextmanager
def make_temp_dir(dirname=None):
    temp_dir = mkdtemp(dir=dirname)
    try:
        yield temp_dir
    finally:
        shutil.rmtree(temp_dir)

class Client:
    def __init__(self, uri="http://localhost:8001"):
        # trying to get Mirage URI from environment variable
        self.uri = os.getenv("MIRAGE_URI", uri)

    def login(self, uri):
        """
        Sets new Mirage URI
        :param uri: <string> - http://some_host:port
        """
        self.uri = uri
        os.environ["MIRAGE_URI"] = str(uri)

    def upload(self, args):
        file_name = args['<file_name>']

        if not zipfile.is_zipfile(file_name):
            print("Error! Given file is not a zip file!")
            return

        # reading file
        with open(file_name, 'r') as stream:

            # checking for session or scenario changes
            if args['--session'] or args['--scenario']:
                # changing yaml configuration file with updated scenario or session values
                stream = self._change_config(file_name, args)

            # preparing data
            files = [('files', (file_name, stream, 'application/zip'))]
            data = {}

            resp = requests.post(url=self.uri + "/api/v2/scenarios/upload",
                                 files=files, data=data)

            if resp.status_code == 200:
                for k, v in resp.json().items():
                    print("%s: %s" % (k, v))

            if resp.status_code == 422:
                print("Scenario or session already exists, use optional commands "
                      "[--session=<session_name>] [--scenario=<scenario_name>] to override scenario or session that is "
                      "provided in .yaml configuration file.")
                print("Message from server: %s" % resp.text)

            else:
                print("Something went wrong, status code: %s" % resp.status_code)
                print("Mirage response: %s" % resp.text)

    def _change_config(self, file_name, args):
        """
        Changing configuration file

        :param file_name:
        :param args:
        :return:
        """
        with make_temp_dir(dirname="tmp") as temp_dir:
            with zipfile.ZipFile(file_name) as zipf:
                zipf.extractall(path=temp_dir)
                files = zipf.namelist()

                for f in reversed(files):
                    if f.endswith(".yaml"):
                        # reading yaml file
                        config = None
                        with open(temp_dir + "/" + f, 'r') as stream:
                            try:
                                config = yaml.load(stream)
                                if args['--session']:
                                    config['recording']['session'] = args['--session']
                                if args['--scenario']:
                                    config['recording']['scenario'] = args['--scenario']
                            except Exception as ex:
                                print("Failed to read .yaml file. Got error: %s" % ex)

                            # configuration changed, writing file
                        with open(temp_dir + "/" + f, 'w') as stream:
                            yaml.dump(config, stream)

                output = StringIO()
                with zipfile.ZipFile(output, 'w') as my_memory_zip:
                    for f in files:
                        my_memory_zip.write(temp_dir + "/" + f, arcname=f)

                return output.getvalue()

if __name__ == '__main__':
    arguments = docopt(__doc__, version=version)

    c = Client()
    # login case
    if arguments['login']:
        c.login(arguments['<mirage_uri>'])
    # uploading scenario
    if arguments['upload']:
        c.upload(arguments)
