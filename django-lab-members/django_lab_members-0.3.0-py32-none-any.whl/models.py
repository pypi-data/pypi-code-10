from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from datetime import datetime
from filer.fields.image import FilerImageField

if 'cms_lab_members' in settings.INSTALLED_APPS:
    from cms.models.fields import PlaceholderField

YEARS = tuple((yr, yr) for yr in reversed(range(1960, datetime.now().year + 1)))


class Position(models.Model):

    class Meta:
        ordering = ['title']
        verbose_name = "Position"
        verbose_name_plural = "Positions"

    title = models.CharField(u'title',
        blank=False,
        default='',
        help_text=u'Please enter a title for this position',
        max_length=64,
        unique=True,
    )

    def __str__(self):
        return self.title


class ScientistBase(models.Model):

    class Meta:
        abstract = True
        ordering = ['full_name']
        verbose_name = "Scientist"
        verbose_name_plural = "Scientists"

    full_name = models.CharField(u'full name',
        blank=False,
        default='',
        help_text=u'Please enter a full name for this scientist',
        max_length=64,
        unique=True,
    )

    slug = models.SlugField(u'slug',
        blank=False,
        default='',
        help_text=u'Please enter a unique slug for this scientist',
        max_length=64,
    )

    title = models.ForeignKey('lab_members.Position',
        blank=True,
        default=None,
        help_text=u'Please specify a title for this scientist',
        null=True,
        on_delete=models.PROTECT,
        related_name='current_scientist_set',
    )

    email = models.EmailField(u'email address',
        null=True,
        help_text=u'Please enter email address',
    )

    website_url = models.URLField('website URL',
        blank=True,
        help_text='If this scientist has a separate website, enter the URL.',
    )

    website_name = models.CharField('website name',
        blank=True,
        help_text='Enter a name to display for the website. ' \
                  'Default is the URL of the site.',
        max_length=64,
    )

    current = models.BooleanField(u'current lab member',
        default=True,
        help_text=u'Please specify whether scientist is a current lab member',
    )

    alumni_current_institution = models.ForeignKey('lab_members.Institution',
        blank=True,
        default=None,
        help_text=u"If former lab member, please enter the scientist's new institution",
        null=True,
        on_delete=models.PROTECT,
    )

    alumni_current_title = models.ForeignKey('lab_members.Position',
        blank=True,
        default=None,
        help_text=u"If former lab member, please enter the scientist's new title",
        null=True,
        on_delete=models.PROTECT,
        related_name='alumni_scientist_set',
    )

    alumni_redirect_url = models.URLField(u'alumni redirect URL',
        null=True,
        blank=True,
        help_text=u"If former lab member, please enter the scientist's new URL"
    )

    photo = FilerImageField(
        null=True,
        blank=True,
        help_text=u'Please upload an photo of this scientist',
        on_delete=models.PROTECT,
    )

    visible = models.BooleanField('visible',
        default=True,
        help_text='Display this scientist?',
    )

    def __str__(self):
        return self.full_name


class Scientist(ScientistBase):

    if 'cms_lab_members' in settings.INSTALLED_APPS:
        personal_interests = PlaceholderField(u'personal interests',
            related_name='personal_interests',
        )

        research_interests = PlaceholderField(u'research interests',
            related_name='research_interests',
        )

        publications = PlaceholderField(u'publications',
            related_name='publications',
        )

        sidebar = PlaceholderField(u'scientist sidebar',
            related_name='scientist_sidebar',
        )

    else:
        personal_interests = models.TextField(u'personal interests',
            blank=True,
            default='',
            help_text=u'Please write a personal interests blurb for this scientist'
        )

        research_interests = models.TextField(u'research interests',
            blank=True,
            default='',
            help_text=u'Please write a research interests blurb for this scientist'
        )


class Institution(models.Model):

    class Meta:
        ordering = ['name']
        verbose_name = "Institution"
        verbose_name_plural = "Institutions"

    name = models.CharField(u'institution name',
        help_text=u'Please enter the institution attended',
        max_length=64,
        unique=True,
    )

    def __str__(self):
        return self.name


class Degree(models.Model):

    class Meta:
        ordering = ['title']
        verbose_name = "Degree"
        verbose_name_plural = "Degrees"

    title = models.CharField(u'degree title',
        help_text=u'Please enter a degree type',
        max_length=64,
        unique=True,
    )

    def __str__(self):
        return self.title


class Field(models.Model):

    class Meta:
        ordering = ['label']
        verbose_name = "Field"
        verbose_name_plural = "Fields"

    label = models.CharField(u'field of study',
        help_text=u'Please enter a field of study',
        max_length=64,
        unique=True,
    )

    def __str__(self):
        return self.label


class Advisor(models.Model):

    class Meta:
        ordering = ['full_name']
        verbose_name = "Advisor"
        verbose_name_plural = "Advisors"

    full_name = models.CharField(u'advisor name',
        help_text=u"Please enter advisor's name",
        max_length=64,
        unique=True,
    )

    url = models.URLField(u'advisor website',
        null=True,
        blank=True,
        help_text=u"Please enter advisor's website",
    )

    def __str__(self):
        return self.full_name


class Records(models.Model):

    class Meta:
        abstract = True

    institution = models.ForeignKey('lab_members.Institution',
        help_text=u'Please enter the institution attended',
        on_delete=models.PROTECT,
    )

    field = models.ForeignKey(u'lab_members.Field',
        null=True,
        blank=True,
        help_text=u'Please specify the field studied',
        on_delete=models.PROTECT,
    )

    scientist = models.ForeignKey('lab_members.Scientist')

    advisors = models.ManyToManyField(Advisor,
        blank=True,
        help_text=u"Please select advisor's name (or multiple co-advisors).<br>",
        related_name='%(app_label)s_%(class)s_records',
    )

    def clean(self):
        if self.year_start and self.year_end and self.year_start > self.year_end:
            raise ValidationError("'Year Started' cannot come after 'Year Ended'.")


class Education(Records):

    class Meta:
        ordering = ['-year_start', '-year_end']
        verbose_name = "Education record"
        verbose_name_plural = "Education records"

    degree = models.ForeignKey(u'lab_members.Degree',
        null=True,
        blank=True,
        help_text=u'Please specify the degree granted',
        on_delete=models.PROTECT,
    )

    year_start = models.IntegerField(u'year started',
        null=True,
        blank=True,
        choices=YEARS,
        help_text=u'Please specify the year started',
    )

    year_end = models.IntegerField(u'year degree granted (or study ended)',
        null=True,
        blank=True,
        choices=YEARS,
        help_text=u'Please specify the year finished',
    )

    def __str__(self):
        if self.year_start and self.year_end:
            years = " - ".join([str(self.year_start), str(self.year_end)])
        elif self.year_start:
            years = " - ".join([str(self.year_start), "Present"])
        elif self.year_end:
            years = str(self.year_end)
        else:
            years = "No dates given"

        return years


class Employment(Records):

    class Meta:
        ordering = ['-year_start', '-year_end']
        verbose_name = "Employment record"
        verbose_name_plural = "Employment records"

    position = models.ForeignKey('lab_members.Position',
        help_text=u'Please enter a title for this position',
        on_delete=models.PROTECT,
    )

    year_start = models.IntegerField(u'year started',
        null=True,
        choices=YEARS,
        help_text=u'Please specify the year started',
    )

    year_end = models.IntegerField(u'year ended',
        null=True,
        blank=True,
        choices=YEARS,
        help_text=u'Please specify the year finished',
    )

    def __str__(self):
        if self.year_start and self.year_end:
            years = " - ".join([str(self.year_start), str(self.year_end)])
        elif self.year_start:
            years = " - ".join([str(self.year_start), "Present"])
        elif self.year_end:
            years = "'Year started' is required"    # This should never happen
        else:
            years = "No dates given"

        return years
