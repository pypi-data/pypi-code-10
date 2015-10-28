#! /usr/bin/env python
"""Mirage Command Line Client.
Usage:
  mirage env
  mirage new <scenario_name>
  mirage remove <scenario_name>
  mirage scenarios [-d]
  mirage begin --scenario=<scenario_name> --session=<session_name> --mode=<record|playback>
  mirage end --scenario=<scenario_name> [--session=<session_name>]
  mirage upload <file_name> [--session=<session_name>] [--scenario=<scenario_name>]
  mirage -h | --help
  mirage --version

Examples:
  export MIRAGE_URI=http://mirage_ip:8001
  mirage new scenario_x
  mirage begin --scenario=scenario_x --session=ses_x --mode=record
  mirage end --scenario=scenario_x
  mirage begin --scenario=scenario_x --session=ses_x --mode=playback
  mirage end --scenario=scenario_x
  mirage remove scenario_x

Options:
  -h --help     Show this screen.
  --version     Show version.
  -d            Show details.
"""
from docopt import docopt
import requests
import json
import os
import zipfile
import yaml
import contextlib
import shutil
from cStringIO import StringIO
from tempfile import mkdtemp
from . import version
from terminaltables import AsciiTable


MirageAPI = {
    "scenario_base": "/api/v2/scenarios",
    "scenario_list_detail": "/api/v2/scenarios/detail",
    "scenario": "/api/v2/scenarios/objects/%s",
    "scenario_upload": "/api/v2/scenarios/upload",
    "session_control": "/api/v2/scenarios/objects/%s/action"
}


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

    def show_env(self):
        """
        Show current Mirage endpoint
        """
        print(self.uri)

    def create_scenario(self, scenario_name):
        """
        Creates new scenario
        :param scenario_name: <string> - scenario name
        :return:
        """
        s = requests.Session()
        req = self._create_scenario(scenario_name)

        prepped = req.prepare()
        resp = s.send(prepped, verify=False)

        if resp.status_code == 201:
            print("Scenario %s created." % scenario_name)
        elif resp.status_code == 422:
            print("Failed to create. Scenario %s already exists.")
        else:
            print("Failed to create scenario %s. Got error: %s" % (scenario_name, resp.text))

    def _create_scenario(self, scenario_name):
        """
        Prepares request for scenario creation
        :param scenario_name:
        :return:
        """
        req = requests.Request('PUT', url=self.uri + MirageAPI['scenario_base'],
                               json={"scenario": str(scenario_name)})

        return req

    def list_scenarios(self, detail=False):
        """
        Lists all scenarios.
        :param detail: optional - if supplied gets detailed information about scenarios
        """
        if detail:
            resp = requests.get(url=self.uri + MirageAPI['scenario_list_detail'])
            if resp.status_code == 200:
                scenario_list = resp.json()['data']
                # output scenarios
                # scenario_name session_name status loaded last_used space_used stub_count recorded
                # creating table data list with headers
                table_data = [['Scenario', 'Session', 'Status', 'Loaded', 'Last Used', 'Size (KB)', 'Stubs', 'Recorded']]
                for scenario in scenario_list:
                    session_name, status, loaded, last_used = self._get_session_information(scenario['sessions'])

                    row = [scenario['name'], session_name, status, loaded, last_used, str(scenario['space_used_kb']),
                           str(scenario['stub_count']), scenario['recorded']]
                    table_data.append(row)

                table = AsciiTable(table_data)
                print(table.table)
            else:
                print("Failed to retrieve detailed scenario list. Got response: %s" % resp.text)

        else:
            resp = requests.get(url=self.uri + MirageAPI['scenario_base'])
            if resp.status_code == 200:
                scenario_list = resp.json()['data']
                table_data = [['Scenario', 'Scenario details href']]

                for scenario in scenario_list:
                    row = [scenario['name'], scenario['scenarioRef']]
                    table_data.append(row)

                table = AsciiTable(table_data)
                print(table.table)
            else:
                print("Failed to retrieve scenario list. Got response: %s" % resp.text)

    @staticmethod
    def _get_session_information(sessions):
        """
        Prepares session data
        :param sessions:
        :return:
        """
        status = '-'
        name = '-'
        last_used = '-'
        loaded = '-'
        if sessions:
            # taking first session
            status = sessions[0].get('status', '-')
            name = sessions[0].get('name', '-')
            last_used = sessions[0].get('last_used', '-')
            # making sure we don't return None
            if not last_used:
                last_used = '-'
            loaded = sessions[0].get('loaded', '-')
            if not loaded:
                loaded = '-'
        return name, status, loaded, last_used

    def begin_session(self, scenario_name, session, mode):
        """
        Begins sessions. Does not try to create scenario.
        :param scenario_name: <string>
        :param session: <string>
        :param mode: <string>
        """
        s = requests.Session()
        req = self._begin_session(scenario_name, session, mode)

        prepped = req.prepare()
        resp = s.send(prepped, verify=False)

        if resp.status_code == 200:
            print("Session %s started successfully. Scenario: %s, Mode: %s" % (scenario_name, session, mode))
        else:
            print("Failed to start session %s for scenario %s. Got error: %s" % (session, scenario_name, resp.text))

    def _begin_session(self, scenario_name, session, mode):
        """
        Prepares request for session begin
        :param scenario_name: <string>
        :param session: <string>
        :param mode: <string>
        :return:
        """
        payload = {
            "begin": None,
            "session": str(session),
            "mode": str(mode)
        }
        api = MirageAPI['session_control']
        req = requests.Request('POST', url=self.uri + api % scenario_name,
                               json=payload)
        return req

    def end_session(self, scenario_name, session=None):
        """
        Ends session or sessions for specific scenario.
        :param scenario_name: required
        :param session: - optional, if omitted - ends all sessions for scenario
        """
        s = requests.Session()
        req = self._end_session(scenario_name, session)

        prepped = req.prepare()
        resp = s.send(prepped, verify=False)

        if resp.status_code == 200:
            print("Session(-s) ended successfully.")
        else:
            print("Something went wrong. Status code: %s. Got message: %s" % (resp.status_code, resp.text))

    def _end_session(self, scenario_name, session=None):
        """
        Prepares request for end session
        :param scenario_name: required
        :param session: - optional, if omitted - ends all sessions for scenario
        """
        if session:
            # ending specific session
            payload = {
                "end": None,
                "session": session
            }
        else:
            # ending all sessions for scenario
            payload = {
                "end": "sessions"
            }

        api = MirageAPI['session_control']
        req = requests.Request('POST', url=self.uri + api % scenario_name,
                               json=payload)
        return req

    def remove_scenario(self, scenario_name):
        """
        Removes specified scenario
        :param scenario_name:
        :param force:
        """
        s = requests.Session()
        req = self._remove_scenario(scenario_name)

        prepped = req.prepare()
        resp = s.send(prepped, verify=False)

        if resp.status_code == 200:
            print("Scenario %s removed successfully." % scenario_name)
        else:
            print("Something went wrong. Status code: %s. Got message: %s" % (resp.status_code, resp.text))

    def _remove_scenario(self, scenario_name):
        """

        Prepares request for scenario delete
        :param scenario_name:
        :param force:
        """
        api = MirageAPI['scenario']
        req = requests.Request('DELETE', url=self.uri + api % scenario_name)
        return req

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

            resp = requests.post(url=self.uri + MirageAPI['scenario_upload'],
                                 files=files, data=data)

            if resp.status_code == 200:
                for k, v in resp.json().items():
                    print("%s: %s" % (k, v))
            elif resp.status_code == 422:
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
        with make_temp_dir(dirname="/tmp") as temp_dir:
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


def main():
    arguments = docopt(__doc__, version=version)
    c = Client()

    # showing current Mirage endpoint
    if arguments['env']:
        c.show_env()
    # creating new scenario
    if arguments['new']:
        c.create_scenario(arguments['<scenario_name>'])
    # removing scenario
    if arguments['remove']:
        c.remove_scenario(arguments['<scenario_name>'])
    # list scenarios
    if arguments['scenarios']:
        c.list_scenarios(arguments['-d'])
    # begin new session
    if arguments['begin']:
        c.begin_session(arguments['--scenario'], arguments['--session'], arguments['--mode'])
    # end session or sessions
    if arguments['end']:
        c.end_session(arguments['--scenario'], arguments['--session'])
    # uploading scenario
    if arguments['upload']:
        c.upload(arguments)
