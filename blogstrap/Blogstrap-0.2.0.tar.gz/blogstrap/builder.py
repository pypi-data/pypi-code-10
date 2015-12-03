# Copyright 2015 Joe H. Rahme <joehakimrahme@gmail.com>
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.
import os


APP_TEMPLATE = """import os

from blogstrap import create_app

BASE = os.path.dirname(os.path.abspath(__file__))
config = lambda x: os.path.join(BASE, x)

application = create_app(config('.blogstrap.conf'))

if __name__ == '__main__':
    application.run()
"""

CONF_TEMPLATE = """
BLOGROOT = "."
BLOGTITLE = "Generated with BloGstrap"
THEME = "simplex"
DEBUG = True
"""


def build(args):
    app_path = os.path.join(args.target, 'wsgi.py')
    conf_path = os.path.join(args.target, '.blogstrap.conf')

    if not os.path.exists(args.target):
        os.makedirs(args.target)

    with open(app_path, 'w') as f:
        f.write(APP_TEMPLATE)

    with open(conf_path, 'w') as f:
        f.write(CONF_TEMPLATE)
