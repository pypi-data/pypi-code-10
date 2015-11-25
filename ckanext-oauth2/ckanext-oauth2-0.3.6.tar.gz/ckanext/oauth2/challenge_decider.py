# Copyright (c) 2014 CoNWeT Lab., Universidad Politécnica de Madrid

# This file is part of OAuth2 CKAN Extension.

# OAuth2 CKAN Extension is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# Wirecloud is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with Wirecloud.  If not, see <http://www.gnu.org/licenses/>.

import logging

from repoze.who.interfaces import IChallengeDecider
from webob import Request
from zope.interface import directlyProvides

log = logging.getLogger(__name__)


def oauth_challenge_decider(environ, status, headers):

    request = Request(environ)

    if status.startswith('401 ') and request.path.startswith('/user/login'):
        # Only log the user when s/he tries to log in. Otherwise, the user will be
        # redirected to the main page where an error will be shown
        return True
    elif 'repoze.whoplugins.openid.openid' in environ:
        # handle the openid plugin too
        return True

    return False

directlyProvides(oauth_challenge_decider, IChallengeDecider)
