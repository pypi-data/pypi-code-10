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

"""
Redlink Python SDK: C{https://github.com/redlink-gmbh/redlink-python-sdk}
"""

__version__ = "1.0.1"
__authors__ = "Sergio Fernandez"
__license__ = "Apache License, Version 2.0"
__url__ = "https://github.com/redlink-gmbh/redlink-python-sdk"
__contact__ = "support@redlink.io"
__date__ = "2015-10-28"
__agent__ = "RedlinkPythonSDK/%s" % __version__

from .analysis import RedlinkAnalysis
from .data import RedlinkData


def create_analysis_client(key):
    """
    Create an instance of a Redlink Analysis Client

    @type  key: str
    @param key: api key

    @rtype: C{RedlinkAnalysis}
    @return: analysis client
    """
    return RedlinkAnalysis(key)


def create_data_client(key):
    """
    Create an instance of a Redlink Dara Client

    @type  key: str
    @param key: api key

    @rtype: C{RedlinkData}
    @return: data client
    """
    return RedlinkData(key)
