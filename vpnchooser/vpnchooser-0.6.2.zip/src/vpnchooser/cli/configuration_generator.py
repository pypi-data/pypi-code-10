# -*- encoding: utf-8 -*-

from getpass import getpass

from pkg_resources import resource_string
from paramiko.client import (
    SSHClient,
    MissingHostKeyPolicy,
)


class ConfigurationGenerator(MissingHostKeyPolicy):
    """
    Generates a config file from given input.
    """

    def __init__(self, file_location):
        self.file_location = file_location

    def request_host(self):
        self.host = input("Router SSH host: ")

    def request_username(self):
        self.username = input("Router SSH username: ") or "root"

    def request_password(self):
        self.password = getpass("Router SSH password: ")

    def request_database(self):
        print("(see http://docs.sqlalchemy.org/en/latest/core/engines.html )")
        self.database = input("Database url (sqlite:///test.db): ")

    def request_redis(self):
        redis = input("Host and Port for redis (127.0.0.1:6379): ")
        self.redis = redis or "127.0.0.1:6379"

    def request_data(self):
        self.request_host()
        self.request_username()
        self.request_password()
        self.request_database()
        self.request_redis()

    def generate(self):
        print("Generating Configuration file")
        self.request_data()
        print("Connecting host to get ssh host key and check your "
              "credentials.")
        self.verify()
        self.write_config()

    def write_config(self):
        config_bytes = resource_string('vpnchooser', 'template.cfg')
        config = config_bytes.decode('utf-8')
        written_config = config % dict(
            username=self.username,
            password=self.password,
            host=self.host,
            host_key=self.host_key,
            broker_url=self.redis,
            database=self.database
        )
        with open(self.file_location, 'w') as f:
            f.write(written_config)

    def verify(self):
        client = SSHClient()
        client.set_missing_host_key_policy(self)
        client.connect(
            self.host,
            username=self.username,
            password=self.password,
        )

    def missing_host_key(self, client, hostname, key):
        """
        Called when an `.SSHClient` receives a server key for a server that
        isn't in either the system or local `.HostKeys` object.  To accept
        the key, simply return.  To reject, raised an exception (which will
        be passed to the calling application).
        """
        self.host_key = key.get_base64()
        print("Fetched key is: %s" % self.host_key)
        return


class DockerConfigurationGenerator(ConfigurationGenerator):
    """
    Configuration generator for generating the configuration
    file for docker containers.
    """

    def request_database(self):
        self.database = "sqlite:////data/vpnchooser.db"

    def request_redis(self):
        self.redis = "redis:6379"
