"""

Copyright 2015 Guoliang Li

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

"""

import imp
import os


def get_google_api_key():
    config_folder = os.path.join(os.path.expanduser('~'), '.rabbit_youtube')
    if not os.path.exists(config_folder):
        os.makedirs(config_folder)

    config_file = os.path.join(config_folder, 'config.py')
    if not os.path.isfile(config_file):
        api_key = raw_input('no config file found, please input your google api key:')
        f = open(config_file, 'w+')
        f.write("api_key='%s'\n" % api_key)
        f.close()
    app_config = imp.load_source('', config_file)
    return app_config.api_key
