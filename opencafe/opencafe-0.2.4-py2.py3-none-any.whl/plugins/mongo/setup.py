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
from setuptools import setup, find_packages

setup(
    name='cafe_mongo_plugin',
    version='0.0.1',
    description='The Common Automation Framework Engine',
    author='Rackspace Cloud QE',
    author_email='cloud-cafe@lists.rackspace.com',
    url='http://rackspace.com',
    packages=find_packages(),
    namespace_packages=['cafe'],
    install_requires=['pymongo'],
    zip_safe=False)
