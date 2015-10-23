# Copyright (c) 2015 Mirantis, Inc.
#
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

from appcat_glare import base
from glance.common.artifacts import definitions


class HeatTemplate(definitions.ArtifactType, base.AppCatBase):
    __endpoint__ = 'templates'
    environment = definitions.Dict()
    template_version = definitions.String(allowed_values=[
        '2013-05-23', '2014-10-16', '2015-04-30', '2015-10-15'], required=True,
        mutable=False)  # see http://docs.openstack.org/developer/heat/template_guide/hot_spec.html#hot-spec for list of allowed template version
    template = definitions.BinaryObject(required=True)
