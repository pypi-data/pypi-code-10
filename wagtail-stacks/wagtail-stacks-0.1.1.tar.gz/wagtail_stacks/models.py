from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _

from wagtail.wagtailadmin.edit_handlers import (
    StreamFieldPanel,
    MultiFieldPanel,
    FieldPanel
)
from wagtail.wagtailcore.models import Page
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailimages.models import get_image_model

from streamfield_tools.fields import RegisteredBlockStreamField

WAGTAIL_IMAGE_MODEL = get_image_model()


class StacksPageBase(Page):
    keywords = models.CharField(
        _('Keywords'),
        max_length=300,
        blank=True
    )
    facebook_share_text = models.CharField(
        _('Facebook Share Text'),
        max_length=300,
        blank=True
    )
    twitter_share_text = models.CharField(
        _('Twitter Share Text'),
        max_length=110,
        blank=True,
        help_text=(
            "The text to use when sharing this page to Twitter. Limited to "
            "110 characters."
        )
    )
    social_share_image = models.ForeignKey(
        WAGTAIL_IMAGE_MODEL,
        verbose_name=_('Social Share Image'),
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text=(
            ''
        )
    )
    body = RegisteredBlockStreamField(blank=True)

    is_createable = False

    class Meta:
        abstract = True

StacksPageBase.content_panels = Page.content_panels + [
    StreamFieldPanel('body'),
]

StacksPageBase.promote_panels = [
    MultiFieldPanel(Page.promote_panels, "Common page configuration"),
    MultiFieldPanel(
        [
            FieldPanel('keywords'),
            FieldPanel('facebook_share_text'),
            FieldPanel('twitter_share_text'),
            ImageChooserPanel('social_share_image'),
        ],
        "Social Metadata configuration"
    ),
]
