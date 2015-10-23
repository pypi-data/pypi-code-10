from django import test
import json
from os import path

try:
    from unittest import mock
except ImportError:
    import mock

from facebook_datastore import engines
from facebook_datastore import factories
from facebook_datastore import graph_api
from facebook_datastore import models


def get_data_from_file(file_path):
    base_path = path.dirname(__file__)
    with open(path.join(base_path, file_path)) as data_file:
        raw_data = data_file.read()
    data = json.loads(raw_data)
    return graph_api.get_data_object(raw_data, data)


class TestUserProfileEngine(test.TestCase):
    def setUp(self):
        self.data = get_data_from_file("test_data/test_data.json")
        self.expected_facebook_id = 100002364688506
        self.facebook_user = factories.FacebookUserFactory(
            user_id=self.expected_facebook_id)
        self.facebook_user.save()

    @mock.patch('facepy.graph_api.GraphAPI.get')
    def test_if_engine_creates_profile(self, graph_api_get):
        graph_api_get.return_value = self.data

        engine = engines.UserProfileEngine(self.facebook_user)
        engine.perform()

        profile = models.FacebookUserProfile.objects.get(
            facebook_id=self.expected_facebook_id)

        self.assertEqual(self.expected_facebook_id, profile.facebook_id)
        self.assertEqual(self.data['first_name'], profile.first_name)
        self.assertEqual(self.data['last_name'], profile.last_name)
        self.assertEqual('m', profile.gender)
        self.assertEqual(self.facebook_user.id, profile.user.id)


class TestUserLikeEngine(test.TestCase):
    def setUp(self):
        self.data = get_data_from_file("test_data/test_likes_data.json")
        self.facebook_id = 100002364688506
        self.facebook_user = factories.FacebookUserFactory(
            user_id=self.facebook_id)

    @mock.patch('facepy.graph_api.GraphAPI.get')
    def test_if_engine_creates_likes(self, graph_api_get):
        graph_api_get.return_value = [self.data]
        engine = engines.UserLikeEngine(self.facebook_user)
        engine.perform()
        likes = models.FacebookUserLike.objects.filter(
            user__id=self.facebook_user.id)
        self.assertEqual(3, likes.count())
        like = likes.get(name='DajeRade.com')
        self.assertEqual('Website', like.category)
