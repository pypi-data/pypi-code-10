import itertools

from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.core.validators import URLValidator
from django.db import models
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _

from mptt.models import MPTTModel, TreeForeignKey

from .managers import ItemManager


class ItemBase(MPTTModel):
    """
    Model managing the items without tree inheritance and providing the basic fields and behaviours.

    For the hierarchy of items, the class is using the 'mptt' module, see https://django-mptt.github.io/django-mptt/

    Each item has a url associated that generates a href at save. This behaviour is used to optimize the processing
    required in case the field uses complex value like django url pattern.
    """
    parent = TreeForeignKey(
        blank=True,
        db_index=True,
        null=True,
        related_name='children',
        to='self')
    name = models.CharField(
        _('Name'), max_length=255)
    slug = models.SlugField(unique=True, verbose_name=_(u'Slug'), max_length=150)

    url = models.CharField(
        _('Url'), blank=True, null=True, max_length=255)
    content_type = models.ForeignKey(ContentType, null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    content_object = GenericForeignKey('content_type', 'object_id')
    href = models.CharField(
        _('Link'), blank=True, null=True, max_length=255)

    access_loggedin = models.BooleanField(
        _('Logged in only'),
        help_text=_('Check it to grant access to this item to authenticated users only.'),
        db_index=True, default=False)
    access_group = models.ManyToManyField(
        Group, verbose_name=_('User must belong to one of these groups'), blank=True)
    access_permissions = models.ManyToManyField(
        Permission, verbose_name=_('User must have one of these permissions'), blank=True)

    css_class = models.CharField(
        _('Css class'), blank=True, null=True, max_length=100, help_text=_('Specify a css class.'))
    is_new_tab = models.BooleanField(
        _('New tab'), db_index=True, default=False,
        help_text=_('The link should open in a new tab.'))

    objects = ItemManager()

    class Meta:
        abstract = True
        verbose_name = _(u"navigation item")
        verbose_name_plural = _(u"navigation items")

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.__unicode__()

    def url_is_valid(self):
        """
        Checks if the 'url' property of the object is a valid url.

        :returns:  bool -- the url is valid or not.
        """
        if self.url:
            val = URLValidator()
            try:
                val(self.url)
                return True
            except ValidationError:
                pass
        return False

    def url_is_pattern(self):
        """
        Checks if the 'url' property of the object is a django url pattern.

        :returns:  bool -- the url is a django url pattern or not.
        """
        if self.url:
            try:
                reverse(self.url)
                return True
            except:
                pass
        return False

    def generate_unique_slug(self):
        """
        Ensures uniqueness of slug, inspired from
        https://keyerror.com/blog/automatically-generating-unique-slugs-in-django
        """
        unique_slug = orig = slugify(self.__str__())
        for x in itertools.count(1):
            if not self.__class__.objects.filter(slug=unique_slug).exists():
                break
            unique_slug = '%s-%d' % (orig, x)
        return unique_slug

    def save(self, *args, **kwargs):
        """
        Overrides the parent class, mostly to generate and store the href field from the url field and
        generates a slug if empty.
        """

        self.href = ''
        if self.url:
            # First try to see if the link is a url
            if self.url_is_valid():
                self.href = self.url
            # Otherwise check if the url is a django pattern
            elif self.url_is_pattern():
                self.href = reverse(self.url)
            # Finally store the value if the url field looks like a relative url
            elif self.url.startswith('/'):
                self.href = self.url
        elif self.content_object:
            self.href = self.content_object.get_absolute_url()

        # store the base field
        if not self.slug:
            self.slug = self.generate_unique_slug()
        super(ItemBase, self).save(*args, **kwargs)


class Item(ItemBase):
    """
    Default Item class inheriting unaltered from ItemBase.
    """
