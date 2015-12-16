import argparse
import json
import os
import base64
import urllib2

import oneid.keychain
import oneid.service
import session


class Service(object):
    """
    Base Service that all services subclass

    :param session: session that manages the current user's
      credentials and settings
    :type session: session.CLISession
    """
    request_uri = None

    def __init__(self, active_session):
        self._session = active_session

    def run(self, *args):
        """
        oneid-cli will first parse for the service,
        if a valid service is found, it will pass the remaining
        args to the service for the service to parse
        """
        raise NotImplementedError


class Configure(Service):
    """
    Store json dump of credentials in ~/.oneid/credentials

    :Example:

        $ oneid-cli configure

    """
    def _touch(self, file_path):
        """
        Make sure a file exists before trying to open

        :param file_path: absolute path to file that needs created
        """
        with open(file_path, 'a'):
            os.utime(file_path, None)

    def update_credential(self, access_id, access_secret, aes_key, project=None):
        """
        Create or update stored configuration file

        :param access_id: oneID Developer portal Access ID for the project
        :param access_secret: Project's secret key, DER formatted private key
        :type access_id: str()
        :type access_secret: str()
        """
        if access_id is None or access_secret is None:
            raise ValueError('Access ID and Access Secret are'
                             'required to configure')

        credential_path = os.path.join(self._session.oneid_config_path(), 'credentials')

        if not os.path.exists(self._session.oneid_config_path()):
            os.mkdir(self._session.oneid_config_path())
            self._touch(credential_path)
        elif not os.path.exists(credential_path):
            self._touch(credential_path)

        with open(credential_path, 'rb+') as credential_file:
            try:
                credentials = json.load(credential_file)
            except ValueError:
                credentials = dict()

            # seek back to the start of the file
            credential_file.seek(0)

            project_creds = dict()
            project_creds['ID'] = access_id
            project_creds['SECRET'] = access_secret
            project_creds['AES'] = aes_key

            if project:
                credentials[project] = project_creds

            if project is None or credentials.get('DEFAULT') is None:
                # If a project wasn't specified or there isn't a default project
                # set project as default
                credentials['DEFAULT'] = project_creds

            json.dump(credentials, credential_file, sort_keys=True, indent=4)

    def run(self, *args):
        project_id = self._session.project
        access_id = raw_input('ONEID ACCESS ID: ')
        access_secret = raw_input('ONEID ACCESS SECRET: ')
        project_encryption_key = raw_input('PROJECT ENCRYPTION KEY: ')

        self.update_credential(access_id, access_secret, project_encryption_key, project_id)


class Provision(Service):
    """
    Provision a new device with keys

    :Example:

        $ oneid-cli provision --type device --name my-iot-device --public-key abcdefg

    """
    def _parse_service_args(self, *args):
        parser = argparse.ArgumentParser()
        parser.add_argument('--type', '-t', choices=['device', 'server'], required=True, help='Type of device, ')
        parser.add_argument('--name', '-n', required=True, help='The name of the device')
        parser.add_argument('--output', '-o', help='Output directory')
        parser.add_argument('--public-key', help='DER formatted public key')
        return parser.parse_args(args)

    def _add_entity_to_project(self, entity_type, entity_name, device_token, output_dir):
        """
        Provision a device to the specified project

        :param entity_type: Either a server or device.
        :param entity_name: Server or Device name.
        :param device_token: Token for oneID to later validate the entity signature.
        :raises HTTPError: Raised if there are any connection errors
        """
        if not isinstance(device_token, oneid.keychain.Token):
            raise TypeError('Device Token is not a oneID keychain Token')

        if entity_type not in ['device', 'server']:
            raise ValueError('Entity Type MUST be either a server or a device')

        provisioning_endpoint = session.SERVER_ENDPOINT.format(project_id=self._session.project)
        if entity_type == 'device':
            provisioning_endpoint = session.EDGE_DEVICE_ENDPOINT.format(project_id=self._session.project)

        public_key_b64 = base64.b64encode(device_token.public_key_der)

        keys = {entity_type: public_key_b64}
        entity_description = oneid.service.encrypt_attr_value(entity_name,
                                                              self._session.encryption_key)

        try:
            response = self._session.make_api_call(provisioning_endpoint,
                                                   'POST',
                                                   description=json.dumps(entity_description),
                                                   public_keys=json.dumps(keys),
                                                   project=self._session.project)
        except urllib2.HTTPError as e:
            print('Error Communicating with oneID - %s' % provisioning_endpoint)
            print(e)
        else:
            print('Successfully Added {entity_type}: {entity_name}'.format(entity_type=entity_type,
                                                                           entity_name=entity_name))

    def run(self, *args):
        """
        Provision a device with a set of identity and application keys.
        If output not specified, print to console
        If public key not specified, generate a private key and save to output

        :param args: command line argument parser args
        """
        service_args = self._parse_service_args(*args)

        device_token = None
        if not service_args.public_key:
            create_key_choice = raw_input('No public key specified.\n'\
                                          'Would you like me to generate a public/private key pair? [Y/n] : ')
            key_options = {'yes': True,
                           'no': False,
                           'y': True,
                           'n': False,
                           'ye': True}
            if create_key_choice.lower() == '':
                create_key_choice = 'y'

            if create_key_choice.lower() in key_options:
                if key_options[create_key_choice.lower()]:
                    device_token = oneid.service.create_secret_key(service_args.output)
                    if service_args.output is None:
                        print('Here is your new secret key\n'\
                              'SAVE THIS IN A SECURE LOCATION\n')
                        print(device_token.secret_as_pem)

            else:
                print('"%s" is an invalid option. Aborting provisioning' % create_key_choice)

        else:
            # TODO: Specify public key type
            device_token = oneid.keychain.Token.from_public_key(service_args.public_key)

        self._add_entity_to_project(service_args.type, service_args.name, device_token, service_args.output)


