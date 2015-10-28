# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

"""Lava client constants"""

# Internals
LOGGER_NAME = 'lavaclient'
DEFAULT_TIMEOUT = 30
DEFAULT_RETRIES = 3
DEFAULT_RETRY_BACKOFF = 0.2


# Authentication
DEFAULT_AUTH_URL = 'https://identity.api.rackspacecloud.com/v2.0'
CBD_SERVICE_TYPE = 'rax:bigdata'
CBD_SERVICE_NAME = 'cloudBigData'
