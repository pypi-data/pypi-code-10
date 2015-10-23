# Copyright 2015 Rackspace
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from cafe.engine.models.data_interfaces import (
    ConfigSectionInterface, _get_path_from_env)


class EngineConfig(ConfigSectionInterface):

    SECTION_NAME = 'OPENCAFE_ENGINE'

    def __init__(self, config_file_path=None):
        config_file_path = config_file_path or _get_path_from_env(
            'CAFE_ENGINE_CONFIG_FILE_PATH')
        super(EngineConfig, self).__init__(config_file_path=config_file_path)

    @property
    def data_directory(self):
        """
        Provided as the default location for data required by tests.
        """

        return self.get_raw("data_directory")

    @property
    def temp_directory(self):
        """
        Provided as the default location for temp files and other temporary
        output generated by tests (not for logs).
        """

        return self.get_raw("temp_directory")

    @property
    def log_directory(self):
        """
        Provided as the default location for logs.
        It is recommended that the default log directory be used as a root
        directory for subdirectories of logs.
        """

        return self.get_raw("log_directory")

    @property
    def config_directory(self):
        """
        Provided as the default location for test config files.
        """

        return self.get_raw("config_directory")

    @property
    def master_log_file_name(self):
        """
        Used by the engine logger as the default name for the file written
        to by the handler on the root python log (since the root python logger
        doesn't have a name by default).
        """

        return self.get_raw("master_log_file_name")

    @property
    def logging_verbosity(self):
        """
        Used by the engine to determine which loggers to add handlers to by
        default
        """

        return self.get_raw("logging_verbosity")

    @property
    def default_test_repo(self):
        """
        Provided as the default name of the python package containing tests to
        be run.  This package must be in your python path under the name
        provided here.
        """

        return self.get_raw("default_test_repo")
