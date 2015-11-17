from django.db import models


class IframePlugin(models.Model):
    project = models.ForeignKey("projects.Project", null=False, blank=False,
                                related_name="iframes")
    title = models.CharField("Title", max_length=255)
    slug = models.SlugField("Slug")
    url = models.URLField("Iframe URL")
    icon = models.TextField("Base64-encoded icon", max_length=8092, blank=True)
    html = models.TextField("Additional HTML before iframe", max_length=8092,
                            blank=True)
    order = models.PositiveSmallIntegerField("Order", default=0)

    class Meta:
        ordering = ['order', 'title']
