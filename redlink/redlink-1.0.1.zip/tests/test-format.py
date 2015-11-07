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

from nose.tools import assert_equals

from redlink.format import Format, from_mimetype

def test_mimetype_lookup():
    assert_equals(Format.TURTLE, from_mimetype("text/turtle"))
    assert_equals(Format.TURTLE, from_mimetype("text/turtle;charset=UTF-8"))
    assert_equals(Format.JSON, from_mimetype("application/json;charset=UTF-8"))
