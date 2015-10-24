from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import slugify


class CorpUserManager(BaseUserManager):
    def create_user(self, username, password):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        # if not email:
        #     raise ValueError(_('Users must have an email address'))

        user = self.model(
            # email=self.normalize_email(email),
            password=password,
            username=username,
            # first_name=first_name,
            # mid_name=mid_name,
            # last_name=last_name,
            # phone=phone,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            password=password,
            username=username,
        )
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class Corporation(models.Model):

    title = models.CharField(max_length=15, verbose_name=_('Title'))
    slug = models.SlugField(verbose_name=_('Alias'), unique=True)

    def __str__(self):
        return self.title


class CorpUser(AbstractBaseUser, PermissionsMixin):

    username = models.CharField(_('Username'), max_length=30, unique=True, db_index=True)
    slug = models.SlugField(editable=False)
    salt = models.CharField(max_length=20, null=True, blank=True, unique=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = CorpUserManager()

    USERNAME_FIELD = 'username'
    # REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        self.slug = slugify(self.username)
        super(CorpUser, self).save()

    def get_short_name(self):
        return self.person.first_name

    def get_full_name(self):
        return self.person.full_name

    @property
    def is_staff(self):
        return self.is_admin

    # def get_absolute_url(self):
    #     from django.core.urlresolvers import reverse
    #     return reverse('user-detail', kwargs={'slug': self.slug})
