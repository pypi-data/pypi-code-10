from __future__ import absolute_import, unicode_literals

import uuid
import mock
import random

from django.db import models

from dj_oydiv.models import (
    VidyoUserBase,
    VidyoAdmin,
    CryptoText
)
from . import VIDYO_PORTAL_PASSWORD, PACKAGE_BASE


def side_effect(*args, **kwargs):
    return random.randint(1, 1000000)


class CryptoTextTest(CryptoText):
    pass


class TestVidyoMock(VidyoUserBase):
    secret_key = VIDYO_PORTAL_PASSWORD
    client_id = models.CharField(max_length=64)

    def save(self, *args, **kwargs):
        with mock.patch(PACKAGE_BASE + '.rpc_wrapper.user') as mocked:
            mocked.create.side_effect = side_effect
            super(TestVidyoMock, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        with mock.patch(PACKAGE_BASE + '.rpc_wrapper.user'):
            super(TestVidyoMock, self).save(*args, **kwargs)

    @staticmethod
    def normalize_client_id(client_id):
        return client_id

    def get_name(self):
        return str(uuid.uuid4())

    def get_extn(self):
        return random.randint(1, 10000000)


class TestVidyo1(VidyoUserBase):
    secret_key = VIDYO_PORTAL_PASSWORD
    client_id = models.CharField(max_length=64)

    def save(self, *args, **kwargs):
        with mock.patch(PACKAGE_BASE + '.rpc_wrapper.user') as mocked:
            mocked.create.side_effect = lambda *_, **__: random.randint(1, 1000000)
            super(TestVidyo1, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        with mock.patch(PACKAGE_BASE + '.rpc_wrapper.user'):
            super(TestVidyo1, self).save(*args, **kwargs)

    @staticmethod
    def normalize_client_id(client_id):
        return client_id

    def get_name(self):
        return str(uuid.uuid4())

    def get_extn(self):
        return random.randint(1, 10000000)


class TestVidyoRealRPC(VidyoUserBase):
    secret_key = VIDYO_PORTAL_PASSWORD
    client_id = models.CharField(max_length=64)

    @staticmethod
    def normalize_client_id(client_id):
        return client_id

    def get_name(self):
        return str(uuid.uuid4())

    def get_extn(self):
        return random.randint(1, 10000000)


def save_then_retrieve(model, **kwargs):
    T = type(model)
    model.save()

    pk = model.id

    t = T.objects.get(pk=pk)
    for k, v in kwargs.items():
        setattr(t, k, v)
    return t


def create_test_admin(ssl=False, dj_auth_user=None, password=VIDYO_PORTAL_PASSWORD, admin='admin'):
    ad = VidyoAdmin(
        portal_user=admin,
        portal_host='myhost.example.com',
        replay_host='myhost.example.com',
        portal_prefix='431',
        ssl=ssl
    )
    if dj_auth_user:
        ad.dj_auth_user = dj_auth_user
    ad.set_password(password, VIDYO_PORTAL_PASSWORD)
    ad.save()
    return ad


def create_multiple_children(admin, client_ids, child_class=TestVidyoMock, count=10):
    for x in range(count):
        u = child_class(_admin_model=admin)
        u.vidyo_entity_id = str(x + 1000)
        u.client_id = client_ids[x]
        u.extension = str(x)
        u.name = str(x)
        u.set_password(admin.secret_key, 'mysecretdata')
        u.save()


def create_only_child(admin, klass=TestVidyoMock, save=False):
    """creates a TestVidyoModel, with the expectation that no id collisions will happen"""
    u = klass(_admin_model=admin)
    u.vidyo_entity_id = '1'
    u.client_id = '1'
    u.extension = admin.portal_prefix + '1'
    u.name = 'test'
    u.set_password(admin.secret_key, 'mysecretdata')
    if save:
        u.save()
    return u
