from django.db import models
from cms.models import CMSPlugin

class ScientistPluginModel (CMSPlugin):
    scientist = models.ForeignKey('lab_members.Scientist',
        related_name='plugins'
    )

    def __str__(self):
        return self.scientist.full_name
