#! __author__ = 'cltanuki'
from django.db import models


class ABModel(models.Model):

    def get_fields(self):
        return [(field.name, field.value_to_string(self)) for field in self._meta.fields]