from datetime import datetime

from django.db import models
from django.contrib.auth.models import GroupManager
from django.utils.translation import ugettext_lazy as _

from erp.base.enterprise.models import Corporation, CorpUser

SEX_CHOICES = (
    ('m', _('Male')),
    ('f', _('Female')),
)


CAT_CHOICES = (
    ('h', _('Personal')),
    ('w', _('Work')),
    ('m', _('Mobile')),
)


class CorpObject(models.Model):

    title = models.CharField(max_length=15, verbose_name=_('Title'))
    slug = models.SlugField(verbose_name=_('Alias'), unique=True)
    corp = models.ForeignKey(Corporation)
    lat = models.FloatField(_('Latitude'), blank=True, null=True)
    lng = models.FloatField(_('Longitude'), blank=True, null=True)
    #value = models.IntegerField(blank=True, null=True)
    parent = models.ForeignKey('CorpObject', blank=True, null=True)
    city = models.CharField(verbose_name=_('City'), max_length=50)
    street = models.CharField(verbose_name=_('Street'), max_length=50)
    building = models.CharField(verbose_name=_('Building'), max_length=10)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        from django.core.urlresolvers import reverse
        return reverse('obj-detail', args=[str(self.slug)])


class CorpUnit(models.Model):

    title = models.CharField(_('Title'), max_length=80, unique=True)
    slug = models.SlugField(verbose_name=_('Alias'), unique=True)
    corp = models.ForeignKey(Corporation)
    chief = models.ForeignKey(CorpUser, verbose_name=_('Corp unit chief'))
    obj = models.ForeignKey(CorpObject, blank=True, null=True)
    #value = models.IntegerField(blank=True, null=True)
    parent = models.ForeignKey('CorpUnit', blank=True, null=True)

    objects = GroupManager()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        from django.core.urlresolvers import reverse
        return reverse('unit-detail', args=[str(self.slug)])


class Position(models.Model):
    person = models.ForeignKey(to='Person', related_name='positions')
    unit = models.ForeignKey(CorpUnit)
    title = models.CharField(_('Position'), max_length=30)
    since = models.DateField(_('Since'))
    until = models.DateField(_('Until'), null=True, blank=True)

    def __str__(self):
        return self.person.user.username

    def fire(self, date=None):
        self.until = date if date else datetime.now().date()
        self.save()


class Person(models.Model):
    user = models.OneToOneField(CorpUser, verbose_name=_('Personal data'), null=True)
    first_name = models.CharField(verbose_name=_('First name'), max_length=30)
    last_name = models.CharField(verbose_name=_('Last name'), max_length=30)
    mid_name = models.CharField(verbose_name=_('Middle name'), max_length=30, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True, verbose_name=_('Date of birth'))
    sex = models.CharField(choices=SEX_CHOICES, max_length=1)
    avatar = models.ImageField(upload_to='users/avatar', null=True, blank=True)
    post = models.ManyToManyField(CorpUnit, through='Position', verbose_name=_('Position'), editable=False)
    salt = models.CharField(max_length=20, null=True, blank=True, unique=True)

    def __str__(self):
        return self.user.username

    @property
    def full_name(self):
        return self.first_name, self.mid_name if self.mid_name else '', self.last_name
    #
    # @property
    # def salt(self):
    #     if self._salt:
    #         return self._salt
    #     elif self.user.salt:
    #         return self.user.salt
    #     else:
    #         return ''
    #
    # @salt.setter
    # def salt(self, value):
    #     self._salt = value


class EMail(models.Model):
    person = models.ForeignKey(Person, verbose_name=_('E-Mail'), related_name='emails')
    cat = models.CharField(verbose_name=_('Type'), max_length=1, choices=CAT_CHOICES)
    body = models.EmailField(verbose_name=_('E-Mail'))
    notify = models.BooleanField(verbose_name=_('Notification'), default=True)


class Address(models.Model):

    person = models.ForeignKey(Person, verbose_name=_('Address'))


class Phone(models.Model):

    person = models.ForeignKey(Person, verbose_name=_('Phone no.'), related_name='phones')
    cat = models.CharField(verbose_name=_('Type'), max_length=1, choices=CAT_CHOICES)
    country_code = models.IntegerField(verbose_name=_('Country Code'))
    area_code = models.IntegerField(verbose_name=_('Area code'))
    number = models.CharField(max_length=7, verbose_name=_('Subscriber number'))