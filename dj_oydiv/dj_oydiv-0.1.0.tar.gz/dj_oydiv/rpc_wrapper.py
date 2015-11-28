# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

import logging
import copy

import arrow

from django.utils.functional import SimpleLazyObject
from django.core.exceptions import ObjectDoesNotExist

from oydiv_rpc import user
from oydiv_rpc import replay
from oydiv_rpc.member import PortalMember
from oydiv_rpc.exceptions import BaseError

# The entire API:
"""
vidyouser.conference_rpc.authentication_credentials(**kwargs)
vidyouser.conference_rpc.activate(endpoint_id)
vidyouser.conference_rpc.status()
vidyouser.conference_rpc.join_conference()
vidyouser.conference_rpc.exit_conference()

vidyouser.admin_rpc.create() # returns a unique integer id for the account
vidyouser.admin_rpc.delete() # returns ``None`` or raises an Exception
vidyouser.admin_rpc.update(**kwargs) # update the existing account details on the portal.

vidyouser.recording_rpc.start_recording()
vidyouser.recording_rpc.stop_recording()
vidyouser.recording_rpc.all()
vidyouser.recording_rpc.filter(**kwargs)
vidyouser.recording_rpc.get(id)
vidyouser.recording_rpc.delete(id)
"""

logger = logging.getLogger(__name__)


class RPCError(BaseError):
    pass


class Recording(object):
    def __init__(self, record, library_rpc):
        self.id = record.guid
        self.fp = library_rpc.open(record)
        self.start = arrow.get(record.dateCreated)
        self.end = arrow.get(record.endTime).datetime if record.endTime is not None else None
        self.file_bytes = record.fileSize

    def __len__(self):
        """
        Size of the recorded file in bytes.
        """
        return int(self.file_bytes)


class SimpleAdminRPCWrapper(object):
    def __init__(self, hostname, admin_username, admin_password, ssl, **kwargs):
        """
        We don't want to cause an unnecessary RPC requests if the object access
        does not actually require RPC. We defer this by using SimpleLazyObject.
        """
        member = PortalMember(**kwargs)

        self.rpc = SimpleLazyObject(
            lambda: user.User(
                hostname,
                user=admin_username,
                password=admin_password,
                api_type='admin',
                member=member,
                ssl=ssl,
            )
        )

    def create(self):
        return self.rpc.create()

    def delete(self):
        try:
            return self.rpc.delete()
        except user.DoesNotExist as e:
            raise ObjectDoesNotExist(str(e))

    def update(self, **kwargs):
        return self.rpc.update(**kwargs)


class SimpleUserRPCWrapper(object):
    def __init__(self, hostname, username, password, ssl, pin):
        self._pin = pin
        self.rpc = SimpleLazyObject(
            lambda: user.User(hostname, user=username, password=password, ssl=ssl)
        )

    def authenticate_endpoint(self, **kwargs):
        """
        Get information necessary to allow an endpoint to authenticate itself.
        All kwargs are passed to the underlying transport.
        """
        # We modify kwargs
        kwargs = copy.copy(kwargs)
        guest = kwargs.pop('guest', True)
        return self.rpc.endpoint_login_data(guest=guest, **kwargs)

    def activate_endpoint(self, endpoint_id, **kwargs):
        """
        Given an authenticated endpoint, activate it so that calls can be made.
        It is an error to attempt to activate an inactive client, but this is
        not checked.
        """
        return self.rpc.activate_endpoint(endpoint_id, **kwargs)

    def join_conference(self, conference, **kwargs):
        """
        Bring an activated endpoint into a call. It is an error to call this
        on an inactive endpoint.
        """
        if not isinstance(conference, (int, )):
            raise TypeError(
                "Conferences must be referenced by their integer id, or"
                "be a subclass of VidyoUserBase"
            )
        return self.rpc.join_room(None, room_id=conference, pin=self._pin, **kwargs)

    def terminate(self):
        """
        Eject the user's endpoints from all calls, and deauthenticate known
        endpoints.
        """
        self.rpc.log_out()


class SimpleReplayRPCWrapper(object):
    """
    A simple collection of methods for interacting with the given user's recording
    functionality (both control of recording, and lookup of past recordings)
    """

    def __init__(self, portal_hostname, replay_hostname, username, password, ssl, **kwargs):
        """
        As replay recording control and library access happen on two separate
        hosts, we need to create RPC backends for both the portal and the replay.
        The Lazy behaviour means we don't actually hit 2 servers unless such
        methods are called.
        """
        self.library_rpc = SimpleLazyObject(
            lambda: replay.Replay(
                replay_hostname,
                username,
                password,
                ssl=ssl
            )
        )
        self.rpc = SimpleLazyObject(
            lambda: user.User(portal_hostname, user=username, password=password)
        )

    def all(self):
        """ generator of all recordings ordered ascending by date"""
        return (Recording(x, self.library_rpc) for x in self.library_rpc.all_records)

    def get(self, id):
        return Recording(self.library_rpc.open(id), self.library_rpc)

    def filter(self, **kwargs):
        return (Recording(x, self.library_rpc) for x in self.library_rpc.filter(**kwargs))

    def start_recording(self, quality=-1):
        """Start recording the currently active user conference (if any).
        If the user is not in a conference raises LookupError."""
        self.rpc.start_recording(quality=quality)

    def stop_recording(self):
        """
        Stop any current recording for the user. Raises LookupError if no
        recording is in progress.
        Return a uuid suitable for later retrieval with ``get`` or
        `filter(uuid=uuid)``
        """
        return self.rpc.stop_recording()


class VidyoUserBaseSimpleRPCMixin(object):
    """
    Make rpc easy.
    This mixin is just a bunch of properties to abstract the access
    to the underlying RPC library without having to tediously build the RPC
    manually each time.
    """

    RPCError = RPCError

    # We can't use the lru_cache for admin because before save() we don't
    # have a pk, and that prevents the model from being hashable.
    # lru_cache requires hashable arguments
    @property
    def admin_rpc(self):
        return SimpleAdminRPCWrapper(
            self.admin_model.portal_host,
            self.admin_model.portal_user,
            self.admin_model.password,
            self.use_ssl(),
            # All kwargs are passed directly to PortalMember ctor
            name=self.portal_name,
            password=self.password,
            displayName=self.portal_displayname,
            Language=self.portal_language,
            groupName=self.portal_group,
            proxyName=self.portal_proxy,
            extension=self.portal_extension,
            emailAddress=self.portal_email,
            RoleName=self.portal_role,
            description=self.portal_description,
            allowCallDirect=self.can_call,
            allowPersonalMeeting=self.can_host,
            locationTag=self.portal_locationtag
        )

    @property
    def conference_rpc(self):
        return SimpleUserRPCWrapper(
            self.admin_model.portal_host,
            self.portal_name,
            self.password,
            self.use_ssl(),
            self.pin,
        )

    @property
    def recording_rpc(self):
        return SimpleReplayRPCWrapper(
            self.admin_model.portal_host,
            self.admin_model.replay_host,
            self.name,
            self.password,
            self.use_ssl()
        )
