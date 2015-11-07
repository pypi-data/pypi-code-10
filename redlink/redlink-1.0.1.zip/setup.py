# -*- coding: utf8 -*-

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from setuptools import setup

try:
    import six
    py3 = six.PY3
except:
    import sys
    py3 = sys.version_info[0] >= 3

# metadata
if py3:
    import re
    _version_re = re.compile(r'__version__\s*=\s*"(.*)"')
    for line in open('redlink/__init__.py', encoding='utf-8'):
        version_match = _version_re.match(line)
        if version_match:
            version = version_match.group(1)
else:
    import redlink
    version = redlink.__version__

from pip.req import parse_requirements
from pip.download import PipSession
requirements = list(parse_requirements('requirements.txt', session=PipSession()))
requires = [str(r.req.project_name) for r in requirements]
install_requires = [str(r.req) for r in requirements]

setup(
      name = 'redlink',
      version = version,
      description = 'Redlink Python SDK',
      long_description = 'Official SDK to use the Redlink API from Python.',
      license = 'Apache Software License 2.0',
      author = "Sergio Fernandez",
      author_email = "sergio.fernandez@redlink.co",
      url = 'https://github.com/redlink-gmbh/redlink-python-sdk',
      download_url = 'https://github.com/redlink-gmbh/redlink-python-sdk/releases',
      platforms = ['any'],
      packages = ['redlink'],
      requires = requires,
      install_requires = install_requires,
      classifiers =  [
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
      ],
      keywords = 'python redlink api client sdk linkeddata rdf marmotta analysis nlp stanbol',
      use_2to3 = True,
)
