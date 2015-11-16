from django.db import models
from django.contrib.contenttypes.models import ContentType


class Document(models.Model):
  name = models.CharField(max_length=255)
  slug = models.SlugField(max_length=255)
  content_type = models.ForeignKey(ContentType)
  source = models.FileField(upload_to='reports')
  convert_to = models.CharField(max_length=5, null=True, blank=True, choices=(
    ('pdf', 'pdf'),
    ('doc', 'doc'),
    ('docx', 'docx'),
    ('xls', 'xls'),
    ('xlsx', 'xlsx'),
  ))
  merge_with_tos = models.BooleanField(default=False)

  def __str__(self):
    return self.name
