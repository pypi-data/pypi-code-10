import sys
import csv
from osgeo import ogr

from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.core.exceptions import ValidationError

from geokey.categories.models import LookupValue

from .exceptions import DataImportError


class DataImport(models.Model):
    csv_file = models.FileField(upload_to='user-uploads/imports')
    project = models.ForeignKey('projects.Project', related_name='imports')
    category = models.ForeignKey('categories.Category', null=True, blank=True)
    geom_field = models.CharField(max_length=100)
    fields = ArrayField(
        models.CharField(max_length=100), blank=True, null=True)
    imported = ArrayField(models.IntegerField(), default=[])

    def get_lookup_fields(self):
        lookupfields = {}
        for field in self.category.fields.all():
            if field.fieldtype == 'LookupField':
                lookupfields[field.key] = field

        return lookupfields

    def get_field_value(self, key, value):
        if key in self.lookupfields:
            lookup_val, created = LookupValue.objects.get_or_create(
                name=value,
                field=self.lookupfields[key]
            )
            return lookup_val.id
        else:
            return value

    def import_csv(self, user):
        from geokey.contributions.serializers import ContributionSerializer

        contributions = []
        errors = []

        csv.field_size_limit(sys.maxsize)

        with open(self.csv_file.path, 'rU') as csvfile:
            reader = csv.reader(csvfile)

            field_names = next(reader, None)
            line_number = 0
            self.lookupfields = self.get_lookup_fields()

            for row in reader:
                line_number += 1
                properties = {}

                geom_offset = 0
                for idx, column in enumerate(row):
                    if field_names[idx] == self.geom_field:
                        geometry = ogr.CreateGeometryFromWkt(column)
                        geom_offset = 1
                    else:
                        try:
                            key = self.fields[idx - geom_offset]
                            if key != '-1':
                                properties[key] = self.get_field_value(
                                    key, column)
                        except IndexError:
                            pass

                feature = {
                    "location": {
                        "geometry": geometry.ExportToJson()
                    },
                    "properties": properties,
                    "meta": {
                        "category": self.category.id,
                        "status": "pending"
                    }
                }

                serializer = ContributionSerializer(
                    data=feature,
                    context={'user': user, 'project': self.project}
                )

                try:
                    serializer.is_valid(raise_exception=True)
                except ValidationError, e:
                    errors.append({
                        'line': line_number,
                        'messages': e.messages
                    })

                contributions.append(serializer)

        if errors:
            raise DataImportError('CSV import failed.', errors)

        [self.imported.append(c.save().id) for c in contributions]
        self.save()
