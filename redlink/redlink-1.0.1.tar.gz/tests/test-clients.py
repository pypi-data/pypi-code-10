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

from nose.tools import assert_true, raises
from .utils import setup_func, with_setup_args

import redlink


@raises(ValueError)
def test_none_key_analysis_client():
    redlink.create_analysis_client(None)


@raises(ValueError)
def test_none_key_data_client():
    redlink.create_data_client(None)


@raises(ValueError)
def test_empty_key_analysis_client():
    redlink.create_analysis_client("")


@raises(ValueError)
def test_empty_key_data_client():
    redlink.create_data_client("")


@with_setup_args(setup_func)
def test_analysis_client_status(key):
    analysis = redlink.create_analysis_client(key)
    assert_true(analysis.status["accessible"])


@with_setup_args(setup_func)
def test_analysis_client_status(key):
    data = redlink.create_data_client(key)
    assert_true(data.status["accessible"])
