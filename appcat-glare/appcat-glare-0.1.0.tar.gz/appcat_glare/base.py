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


from glance.common.artifacts import definitions


class AppCatBase(object):
    provided_by = definitions.Dict(required=True, mutable=False,
                                   properties={
                                       'name': definitions.String(),
                                       'href': definitions.String(
                                           pattern="^((https?://)[a-z][a-z0-9_-]+(\\.[a-z][a-z0-9_-]+)+(/[a-z0-9\\._/~%\\-\\+&\\#\\?!=\\(\\)@]*)?)|(mailto:[a-z][a-z0-9._-]+@[a-z][a-z0-9_-]+(\\.[a-z][a-z0-9_-]+)+)$"),
                                       'company': definitions.String()
                                   }
                                   )
    supported_by = definitions.Dict(properties={
                                        'name': definitions.String(),
                                        'href': definitions.String(
                                            pattern="^((https?://)[a-z][a-z0-9_-]+(\\.[a-z][a-z0-9_-]+)+(/[a-z0-9\\._/~%\\-\\+&\\#\\?!=\\(\\)@]*)?)|(mailto:[a-z][a-z0-9._-]+@[a-z][a-z0-9_-]+(\\.[a-z][a-z0-9_-]+)+)$"),
                                        'company': definitions.String()
                                    },
                                    mutable=False)
    depends = definitions.ArtifactReferenceList()
    release = definitions.Array(mutable=False,
                                min_size=1,
                                item_type=definitions.String(
                                    allowed_values=[
                                        'Austin', 'Bexar', 'Cactus', 'Diablo',
                                        'Essex', 'Folsom', 'Grizzly',
                                        'Havana', 'Icehouse', 'Juno', 'Kilo',
                                        'Liberty', 'Mitaka']))
    icon = definitions.Dict(
        mutable=False,
        properties={
            "top": definitions.Integer(required=True),
            "left": definitions.Integer(required=True),
            "height": definitions.Integer(required=True),
            "url": definitions.String(required=True, pattern="^((https?://)[a-z][a-z0-9_-]*(\\.[a-z][a-z0-9_-]*)+(/[a-z0-9\\._/~%\\-\\+&\\#\\?!=\\(\\)@]*)?)")
        }
    )
    license = definitions.String(pattern="^(GPL .*)|(Apache .*)|(BSD .*)|(MIT)|(Free <= [0-9]+ (Users|Nodes))|(Multi-licensed OpenSource)|(Other)|(Unknown)$",
                                 required=True,
                                 mutable=False)
    license_url = definitions.String(pattern="^((https?://)[a-z][a-z0-9_-]+(\\.[a-z][a-z0-9_-]+)+(/[a-z0-9\\._/~%\\-\\+&\\#\\?!=\\(\\)@]*)?)$",
                                     mutable=False)
    attributes = definitions.Dict(mutable=False)
