from django.db import models


class SimpleParent(models.Model):

    bar = models.CharField(max_length=256)

    class Mapping:
        bar = ''
