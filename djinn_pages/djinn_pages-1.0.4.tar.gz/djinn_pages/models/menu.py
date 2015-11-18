from django.db import models


class MenuItem(models.Model):

    parent = models.ForeignKey("MenuItem", default=None, null=True, blank=True)
    title = models.CharField(max_length=20)
    url = models.CharField(max_length=256, default="#", null=True, blank=True)
    order = models.IntegerField(default=0)

    def __unicode__(self):
        return self.title

    @property
    def has_sub(self):
        return self.menuitem_set.exists()

    class Meta:
        ordering = ['order']
