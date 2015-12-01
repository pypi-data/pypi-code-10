from django.test import Client

from restify.testing import LiveApiTestCase
from restify.resource import ModelResource, QuerysetResource
from restify.serializers import ModelSerializer

from tests.models import Person


class PersonResource(ModelResource):
    class Meta:
        model = Person
        resource_name = 'person'
        serializer = ModelSerializer(fields=("first_name", "last_name",
                                             ("instrument", ("name",))
                                            ))


class PersonSetResource(QuerysetResource):
    class Meta:
        queryset = Person.objects.filter(first_name__startswith='B')
        resource_name = 'persons'
        serializer = ModelSerializer(fields=("first_name", "last_name"))


class ModelResourceTest(LiveApiTestCase):
    RESOURCE = PersonResource

    def setUp(self):
        Person.objects.create_test_data()

    def test_get_person(self):
        pers = Person.objects.first()
        response = self.get(pk=pers.pk)

        data = {
            "first_name": pers.first_name,
            "last_name": pers.last_name,
            "id": pers.pk,
            "instrument": {
                "id": pers.instrument.pk,
                "name": pers.instrument.name,
            }
        }

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, data)


class ModelResourceTest(LiveApiTestCase):
    RESOURCE = PersonSetResource

    def setUp(self):
        Person.objects.create_test_data()

    def test_get_persons(self):
        response = self.get()

        data = [{'first_name': _.first_name, 'last_name': _.last_name, 'id': _.pk}
                for _ in self.RESOURCE.Meta.queryset]

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, data)