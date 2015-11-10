__author__ = 'Chris Bergh'
import json
import os

AMS_PORT = 'ams-port'
AMS_URL= 'ams-url'
AMS_CONTAINER_NAME = 'container-name'
AMS_IMAGE_REPO = 'image-repo'
AMD_IMAGE_TAG = 'image-tag'


class AMSCommandRunnerConfig(object):
    _config_dict = dict()
    _config_attributes = None

    def __init__(self):
        if self._config_dict is None:
            self._config_dict = dict()
        self._required_config_attributes = [AMS_PORT, AMS_URL, AMS_CONTAINER_NAME, AMS_IMAGE_REPO, AMD_IMAGE_TAG]

    def __str__(self):
        return str(self._config_dict)

    def get(self, attribute):
        if attribute is None:
            return None

        if attribute in self._config_dict:
            return self._config_dict[attribute]
        else:
            return None

    def set(self, attribute, value):
        if attribute is None:
            return
        self._config_dict[attribute] = value

    def init_from_dict(self, set_dict):
        self._config_dict = set_dict
        return self.validate_config()

    def init_from_string(self, jstr):
        try:
            self._config_dict = json.loads(jstr)
        except ValueError, e:
            return False
        return self.validate_config()

    def init_from_file(self, file_json):
        if file_json is None:
            print('AMSCommandLineConfig file path cannot be null')
            rv = False
        else:
            try:
                statinfo = os.stat(file_json)
            except Exception:
                pass
                rv = False
            else:
                if statinfo.st_size > 0:
                    with open(file_json) as data_file:
                        try:
                            self._config_dict = json.load(data_file)
                        except ValueError, e:
                            print('AMSCommandLineConfig: failed json.load check syntax %s. %s' % (file_json, e))
                            rv = False
                        else:
                            rv = True
                else:
                    rv = False
        if rv is False:
            return False
        else:
            return self.validate_config()

    def validate_config(self):
        for v in self._required_config_attributes:
            if v not in self._config_dict:
                print("AMSCommandLineConfig: failed to find %s in AMSCommandLineConfig.json" % v)
                return False
        return True
