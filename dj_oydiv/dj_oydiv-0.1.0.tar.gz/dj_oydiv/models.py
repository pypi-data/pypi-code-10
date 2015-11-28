from __future__ import absolute_import, unicode_literals

import logging
import itertools

from django.utils.translation import ugettext as _
from django.apps import apps
from django.db import models, transaction, IntegrityError
from django.conf import settings
from django.core import validators
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.views.decorators.debug import sensitive_variables
from django.utils import ipv6
from django.utils.decorators import method_decorator
from django.utils.encoding import force_text, force_bytes, python_2_unicode_compatible
from django.utils.timezone import now

from django.contrib.contenttypes.fields import (
    GenericForeignKey,
    GenericRelation,
    ContentType
)

from .utils.random import random_digits, random_string
from .utils.crypto import sym_decrypt_cfb_dict, sym_encrypt_cfb_128
from .rpc_wrapper import VidyoUserBaseSimpleRPCMixin
from .config import config

logger = logging.getLogger(__name__)


VIDYO_LANGUAGES = (
    ('en', _('English')),
    ('de', _('German')),
    ('es', _('Spanish')),
    ('fr', _('French')),
    ('it', _('Italian')),
    ('ja', _('Japanese')),
    ('ko', _('Korean')),
    ('pt', _('Portuguese')),
    ('zh_CN', _('Chinese (Simplified)')),
    ('fi', _('Finnish')),
    ('pl', _('Polish')),
    ('zh_TW', _('Taiwanese')),
    ('th', _('Thai')),
    ('ru', _('Russian'))
)


def _random_pin():
    return random_digits(11)


def _validate_prefix(prefix):
    if (not prefix.isdigit()) or int(prefix) < 1 or int(prefix) > 999:
        raise ValidationError()


def _validate_hostname(host):
    return validators.RegexValidator(
        validators.URLValidator.domain_re,
        message=_("Enter a valid hostname")
    )(host)


def _validate_pin(x):
    if (not x.isdigit()) or len(x) < 2 or len(x) > 11:
        raise ValidationError()


def _is_vidyouserbase(x):
    return issubclass(x, VidyoUserBase)


class CryptoText(models.Model):
    """
    This model stores short amounts of encrypted text.
    """

    ciphertext = models.TextField(editable=False, null=True)

    class Meta:
        abstract = True

    @method_decorator(sensitive_variables())
    def __init__(self, *args, **kwargs):
        self.key = kwargs.pop('key', None)
        data = kwargs.pop('data', None)
        super(CryptoText, self).__init__(*args, **kwargs)
        self.data = data

    @property
    @method_decorator(sensitive_variables())
    def data(self):
        """
        A text string of the decrypted data.
        """
        return force_text(self._decrypt(self.key))

    @data.setter
    @method_decorator(sensitive_variables())
    def data(self, text):
        if text is not None:
            try:
                self._encrypt(self.key, text)
            except AttributeError:
                raise ValueError('decryption failed: Key empty')

    @method_decorator(sensitive_variables())
    def _todict(self):
        """
        retrieve a dict suitable for decryption with sym_decrypt_cfb_128()
        """

        scheme, iv, kdf_iter, kdf_salt, hmac_algo, hmac_hex, ciphertext \
            = self.ciphertext.split("$")

        assert 'KDF:PBKDF2' in scheme
        assert 'CRYPT:AES-128-CFB' in scheme
        assert 'HMAC:SHA256' in scheme
        return {
            'ciphertext_64': force_bytes(ciphertext),
            'aes_iv_64': force_bytes(iv),
            'kdf_salt_64': force_bytes(kdf_salt),
            'kdf_iter': int(kdf_iter),
            'hmac_hex': force_bytes(hmac_hex),
            'hmac_algo': hmac_algo,
        }

    @method_decorator(sensitive_variables())
    def _decrypt(self, key):
        """
        Decrypt the stored data using the given key. Returns a raw bytestring.
        To access the original encoded text, use the ``data`` @property member.
        """
        if not self.ciphertext:
            return None
        try:
            return sym_decrypt_cfb_dict(key, self._todict())
        except:
            raise ValueError('decryption failed: wrong key')

    @method_decorator(sensitive_variables())
    def _encrypt(self, key, cleartext):
        """
        Encrypt the given cleartext
        """
        if len(key) < 8:
            raise ValueError("key too short")
        crypto = sym_encrypt_cfb_128(key, cleartext)
        self.ciphertext = "$".join(map(force_text, (
            'CRYPT:AES-128-CFB_HMAC:SHA256_KDF:PBKDF2',
            crypto['aes_iv_64'],
            crypto['kdf_iter'],
            crypto['kdf_salt_64'],
            'sha256',
            crypto['hmac_hex'],
            crypto['ciphertext_64'],
        )))

    @method_decorator(sensitive_variables())
    def change_key(self, newkey):
        """
        Given a newkey, reencrypts the data with the new key.
        requires @self.key already instantiated
        """
        self._encrypt(newkey, self.data)
        self.key = newkey

    def verify(self):
        # TODO
        pass

    def save(self, *args, **kwargs):
        self.verify()
        super(CryptoText, self).save()


class PasswordCrypt(CryptoText):
    """
    An emulated generic OneToOneField allowing one password per anykind of Model.
    """
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        unique_together = ('content_type', 'object_id')


class VidyoCredentialsMixin(object):
    """
    This mixin abstracts many of the encrypted VidyoPassword get/set
    functionality for all VidyoUser/VidyoAdmin classes.
    """
    @property
    @method_decorator(sensitive_variables())
    def _password_model(self):
        try:
            generic_pass = self._passwordcrypt.get()
        except self._passwordcrypt.model.DoesNotExist:
            return self._passwordcrypt.create()
        return generic_pass

    @property
    @method_decorator(sensitive_variables())
    def password(self):
        try:
            return self._password
        except AttributeError:
            return self.get_password(self.secret_key)

    @password.setter
    @method_decorator(sensitive_variables())
    def password(self, val):
        self.set_password(self.secret_key, val)

    @method_decorator(sensitive_variables())
    def get_password(self, key):
        self.secret_key = key
        try:
            return self._password_model.data
        except ValueError:
            self.secret_key = key
            cryptopass = self._password_model
            cryptopass.key = key
            self._password = cryptopass.data
        return self._password

    @method_decorator(sensitive_variables())
    def decrypt(self, key):
        self.secret_key = key
        self.get_password(key)
        return self

    @method_decorator(sensitive_variables())
    def change_key(self, old_key, new_key):
        if isinstance(self, VidyoAdmin):
            logger.warn("changing all keys for %r", self)
            self._change_all_keys(old_key, new_key)
        try:
            self._password_model.data
        except ValueError:
            self.secret_key = old_key
            cryptopass = self._password_model
            cryptopass.key = old_key
            cryptopass.change_key(new_key)
            cryptopass.save(commit=False)

    @method_decorator(sensitive_variables())
    def set_password(self, auth_user_key, vidyo_password=None):
        self.secret_key = auth_user_key
        if vidyo_password is not None:
            self._password = vidyo_password
        #no password has been set. We have to make sure we have a pk before
        #assigment so saving is deferred to model save.  In that case,
        #if a model is discarded, the password is discarded with it.
        return self

    @method_decorator(sensitive_variables())
    def change_password(self, old_auth_user_key, new_key):
        self.get_password(old_auth_user_key)
        self.password = new_key

    @method_decorator(sensitive_variables())
    def _save_password(self):
        cryptopass = self._password_model
        cryptopass.key = self.secret_key
        try:
            cryptopass.data = self._password
        except AttributeError:
            cryptopass.data = None
        cryptopass.save()

    @method_decorator(sensitive_variables())
    def _change_all_keys(self, old_key, new_key):
        """
        Changing the password is a dangerous and expensive operation, as the
        decryption/encryption needs to be handled for all children.
        We wrap the updates in an atomic transaction, so that no vidyo users can
        be created/modified until this transaction completes.
        This method is part of the mixin to avoid having to overload the admin's
        save() method, and avoid any MRO issues/recursive save() calls etc.
        """
        if not isinstance(self, VidyoAdmin):
            raise TypeError("%s must be called from a VidyoAdmin object")
        with transaction.atomic():
            for child in self.all_vidyo_users():
                child.change_key(old_key, new_key)

    def save(self, *args, **kwargs):
        super(VidyoCredentialsMixin, self).save(*args, **kwargs)
        self._save_password()


@python_2_unicode_compatible
class VidyoAdmin(VidyoCredentialsMixin, models.Model):
    dj_auth_user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        null=True,
        help_text=_("The user to which this VidyoAdmin belongs."),
        verbose_name=_("Assigned Owner")
    )
    _passwordcrypt = GenericRelation(PasswordCrypt)

    #Portal Specific
    portal_user = models.CharField(
        _("API username"),
        help_text=_("The admin/operator user on the VidyoPortal"),
        max_length=255,
        default='admin'
    )
    portal_host = models.CharField(
        _("VidyoPortal hostname"),
        help_text=_("FQDN of the portal"),
        max_length=65535,
        default='example.com',
        validators=[_validate_hostname]
    )
    portal_prefix = models.CharField(
        _("Prefix"),
        help_text=_("Tenant prefix (for multitenant portals)"),
        max_length=4, default='001',
        validators=[_validate_prefix]
    )
    user_proxy = models.CharField(
        _("Default Proxy"),
        help_text=_("Default Proxy name for TCP tunneling of conferences"),
        max_length=128, default=config.DEFAULT_PROXY_NAME
    )
    user_group = models.CharField(
        _("Default Group"),
        help_text=_(
            "Default Group for new accounts. "
            "This is used to limit bandwidth and concurrency on the portal"),
        max_length=128, default=config.DEFAULT_GROUP_NAME
    )
    user_role = models.CharField(
        max_length=128,
        choices=(
            ('Normal', _("Normal")),
            ('Operator', _("Operator")),
            ('Admin', _("Admin"))
        ),
        default=config.DEFAULT_ROLE_NAME,
        editable=False
    )
    user_location_tag = models.CharField(
        _("Location Tag"),
        help_text=_(
            "Default location tag for new users (router affinity)"
            " formultiple router configuration."),
        max_length=128, default=config.DEFAULT_LOCATION_TAG
    )

    # Replay specific
    replay_host = models.CharField(
        _("VidyoReplay hostname"),
        help_text=_("The FQDN of the given tenant's replay"),
        max_length=65535,
        default='example.com',
        null=True,
        blank=True,
        validators=[_validate_hostname]
    )

    # CDR specific
    cdr_enabled = models.BooleanField(
        _("Allow collection of Call Detail Records"),
        default=False
    )
    cdr_port = models.PositiveIntegerField(
        _("MySQL port for CDR access"),
        default=3306
    )
    cdr_host = models.CharField(
        _("MySQL hostname"),
        max_length=65535,
        null=True,
        blank=True,
        validators=[_validate_hostname]
    )
    cdr_password = models.CharField(
        _("MySQL password for CDR access"),
        max_length=128,
        null=True,
        blank=True
    )
    cdr_user = models.CharField(
        _("MySQL user for CDR access"),
        max_length=128,
        default='cdraccess'
    )

    # Authentication
    use_ip_auth = models.BooleanField(_("Client IP whitelisting enabled"), default=True)
    ssl = models.BooleanField(_("SSL enabled VidyoPortal"), default=True)

    def use_ssl(self):
        return self.ssl

    def allowed_ips(self):
        return self.ipmodel_set.iterator()

    def allowed_ips_strings(self):
        return [x.ip for x in self.allowed_ips()]

    def _allowed_cleaned_ip(self, ip):
        try:
            self.ipmodel_set.get(ip=ip)
        except self.ipmodel_set.model.DoesNotExist:
            return False
        return True

    def is_ip_allowed(self, ip):
        if not self.use_ip_auth:
            return True
        try:
            validators.validate_ipv46_address(ip)
        except ValidationError:
            return False
        if ipv6.is_valid_ipv6_address(ip):
            ip = ipv6.clean_ipv6_address(ip)
        return self._allowed_cleaned_ip(ip)

    def all_vidyo_users(self):
        """
        Get a generator that yields all the descendants of ``VidyoUserBase``
        owned by this admin.
        """
        return itertools.chain.from_iterable(
            T.objects.filter(_admin_model=self)
            for T in VidyoUserBase.all_vidyo_user_classes()
        )

    @property
    def user_count(self):
        """
        Number of VidyoUserBase descendants with this model as their parent admin.
        """
        return sum(
            T.objects.filter(_admin_model=self).count()
            for T in VidyoUserBase.all_vidyo_user_classes()
        )

    def __str__(self):
        return 'VidyoAdmin portal user %s' % self.dj_auth_user


@python_2_unicode_compatible
class IPModel(models.Model):
    """IP address foreignKey model for IP address whitelisting."""
    #This model exists so we can include a *list* of ip addresses in
    ip = models.GenericIPAddressField(
        default='127.0.0.1',
        validators=[validators.validate_ipv46_address],
        help_text=_("Add the IP address of every authorised client")
    )
    _admin_model = models.ForeignKey(VidyoAdmin)

    def save(self, *args, **kwargs):
        validators.validate_ipv46_address(self.ip)
        if ipv6.is_valid_ipv6_address(self.ip):
            self.ip = ipv6.clean_ipv6_address(self.ip)
        super(IPModel, self).save(*args, **kwargs)
        #if the ip address is ipv6, we want it sanitized

    def __str__(self):
        return str(self.ip)


@python_2_unicode_compatible
class VidyoUserBase(VidyoUserBaseSimpleRPCMixin, VidyoCredentialsMixin, models.Model):
    """
    Abstract base class mapping to a user account on the portal.
    This class abstracts many of the properties of the VidyoPortal admin/user API
    and offers convenience methods to allow easy access to RPC.

    To use this model, subclass in your app and add the following required fields::

        `client_id`: Anything you want to refer to this model. e.g. integer
        primary-key
        UUID, some string.

    Then override then following methods::

        `normalize_client_id(); staticmethod`: given your ``client_id``, sanitize it,
        and normalize the format for storing in the database.
        `get_name()`: return a unique name for the user as a string. This value is
            used directly on the portal as the account name so it should be unique.
            For example, If you're allowing users to manage their own accounts, you
            could simply return ``firstname.lastname``. For any situation in which
            you're managing the accounts automatically, a guaranteed unique value is
            probably better e.g. UUID string/hash over all credentials/random string.

        `get_extn()`: expected to return an extension for your model during save.
            Most of the time your can simply return a random number, which will
            be appended to the portal extension prefix before save.
    """
    _admin_model = models.ForeignKey(VidyoAdmin)
    _passwordcrypt = GenericRelation(PasswordCrypt)
    vidyo_entity_id = models.PositiveIntegerField(editable=False, null=True)

    created = models.DateTimeField(default=now)
    # All of the `portal_*` attributes are needed to create a member on the portal
    # see `oydiv_rpc.member.PortalMember` for gory implementation details.
    portal_name = models.CharField(max_length=255, unique=True, editable=False)
    portal_displayname = models.CharField(_("Full Name"), max_length=255)
    portal_language = models.CharField(max_length=2, choices=VIDYO_LANGUAGES, default='en')
    portal_group = models.CharField(
        max_length=255, default=config.DEFAULT_GROUP_NAME
    )
    portal_proxy = models.CharField(
        max_length=128, default=config.DEFAULT_PROXY_NAME
    )
    portal_extension = models.CharField(max_length=16, editable=False)
    portal_email = models.EmailField(
        default=config.DEFAULT_MANAGER_EMAIL,
        editable=False
    )
    portal_role = models.CharField(
        max_length=255,
        default=config.DEFAULT_ROLE_NAME,
        editable=False
    )
    portal_description = models.CharField(max_length=1024, editable=False)
    portal_locationtag = models.CharField(
        max_length=255,
        default=config.DEFAULT_LOCATION_TAG,
        editable=False
    )

    pin = models.CharField(
        editable=False,
        max_length=11,
        validators=[_validate_pin],
        default=_random_pin
    )
    # Permissions
    can_call = models.BooleanField(default=False, editable=False)
    can_host = models.BooleanField(default=True, editable=False)
    can_record = models.BooleanField(default=False, editable=False)

    class Meta:
        abstract = True

    @classmethod
    def all_vidyo_user_classes(cls):
        """List all django models that are concrete implementations of this abstract
        base class"""
        return filter(lambda x: issubclass(x, VidyoUserBase), apps.get_models())

    @property
    @method_decorator(sensitive_variables())
    def admin_model(self):
        model = self._admin_model
        try:
            model.decrypt(self.secret_key)
        except AttributeError:
            pass
        return model

    def use_ssl(self):
        return self.admin_model.use_ssl()

    def get_extn_prefix(self):
        """
        Get prefix used for all extensions.
        Unique extensions are *required* by the portal. They must also be
        prefixed by a tenant-global prefix.
        """
        return str(self.admin_model.portal_prefix) + str(self.extn_prefix)

    def get_extn(self):
        """Abstract method expected to be implemented by the client model"""
        raise NotImplementedError()

    def get_name(self):
        """Abstract method expected to be implemented by the client model"""
        raise NotImplementedError()

    @staticmethod
    def normalize_client_id(client_id):
        """Abstract method expected to be implemented by the client model
        This method is used to sanitize the client_id before it is saved in
        the database, and before retrieval, to avoid mismatches caused by
        different representations of the same data. For example, the following
        uuids are identical:
            {000d662f75524339b127bc75d8cd9514}
            000d662f-7552-4339-b127-bc75d8cd9514
        but a database is probably not aware of that.
        """
        return client_id

    @method_decorator(sensitive_variables())
    def default_setup(self):
        """
        This method is used in ``self.``self.save() to set default values
        assigned for the tenant, or overriden on the admin.
        Only values that make sense to be inherited as defaults are inherited.
        This method only exists because Vidyo's API gives no way to query this
        information, and so we treat it as a config value with
        ``_admin_model`` as the source of the config data. It's very ugly.
        """
        if self.pk is None and self._admin_model:
            self.portal_proxy = self.admin_model.user_proxy
            self.portal_group = self.admin_model.user_group
            self.portal_role = self.admin_model.user_role
            # Now set the unique user values
            self.portal_name = self.get_name()
            self.portal_description = self.portal_name
            self.portal_extension = str(self.get_extn())
            self.portal_displayname = self.portal_displayname or _("Anonymous")
            try:
                self.password
            except (ObjectDoesNotExist, IntegrityError):
                self.password = random_string()

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.default_setup()
            try:
                self.vidyo_entity_id = self.admin_rpc.create()
            except self.RPCError as e:
                logger.exception("RPC failed; couldn't create account on portal:%s", str(e))
                # This needs to be vague, because we don't know what sensitive
                # info might be in the portal's exception message.
                raise ValidationError(_("The remote portal could not verify the given data"))
        return super(VidyoUserBase, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        try:
            self.admin_rpc.delete()
        except ObjectDoesNotExist as e:
            # That's actually what we're aiming for, so just ignore it.
            # (Though it's a little fishy so log it)
            logger.exception("Couldn't delete VidyoUser; not found on portal: %s - %s", self, e)
        return super(VidyoUserBase, self).delete(*args, **kwargs)

    def __str__(self):
        return (
            '<%s: %s(%s)> extension:%s client_id:%s entity_id:%s' % (
                self.__class__, self.portal_name, self.portal_displayname,
                self.portal_extension, self.client_id, self.vidyo_entity_id
            )
        )
