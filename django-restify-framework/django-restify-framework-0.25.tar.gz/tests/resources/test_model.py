from django.http import Http404

from restify.testing import RestApiTestCase
from restify.resource import ModelResource

from tests.models import Person


class PersonResource(ModelResource):
    class Meta:
        model = Person
        resource_name = 'person'


class ModelResourceTest(RestApiTestCase):
    RESOURCE = PersonResource

    def setUp(self):
        Person.objects.create_test_data()

    def test_get_person(self):
        pers = Person.objects.first()
        resp = self.get(pk=pers.pk)

        self.assertEqual(resp.json['id'], pers.pk)
        field_names = [_.name for _ in Person()._meta.fields]
        self.assertEqual(set(resp.json.keys()), set(field_names))
