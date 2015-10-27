# -*- coding: utf-8 -*-

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

"""
util
--------------------------------

Util methods for functional tests
"""
import operator


def pick_flavor(flavors):
    """Given a flavor list pick the smallest one."""
    for flavor in sorted(
            flavors,
            key=operator.attrgetter('ram')):
        return flavor


def pick_image(images):
    for image in images:
        if image.name.startswith('cirros') and image.name.endswith('-uec'):
            return image
    for image in images:
        if image.name.lower().startswith('ubuntu'):
            return image
