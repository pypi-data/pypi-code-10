from django.db import models


class StaticContent(models.Model):
    name = models.CharField(
        max_length="4096",
        help_text="Short name used to identify the content object within the admin"
    )

    url = models.CharField(
        max_length="4096",
        unique=True,
        blank=True,
        null=True
    )

    content_type = models.CharField(
        max_length="4096",
        default="text/plain"
    )

    content = models.TextField(
        blank=True,
        null=True
    )

    base64 = models.BooleanField(
        default=False,
        help_text="Check if content is base64 encoded"
    )

    def __unicode__(self):
        return self.name
