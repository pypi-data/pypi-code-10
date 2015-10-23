# -*- coding: utf-8 -*-
import isodate
import logging

from django.contrib.auth.models import User
from django.utils import timezone
from facebook_datastore import graph_api
from facebook_datastore import models
from facebook_datastore import parser

logger = logging.getLogger(__name__)


class BaseEngine(object):
    """
    TODO - handle 500
    """
    def __init__(self, facebook_user):
        super(BaseEngine, self).__init__()
        self.facebook_user = facebook_user

    def should_run(self):
        return True

    def run(self):
        if self.should_run():
            self.perform()

    def perform(self):
        data = self.fetch()
        data = self.parse(data)
        self.save(data)

    def fetch(self):
        raise NotImplementedError

    def parse(self, data):
        raise NotImplementedError

    def save(self, data):
        raise NotImplementedError


class UserProfileEngine(BaseEngine):
    def fetch(self):
        graph = graph_api.get_graph_api(self.facebook_user)
        return graph.get('me?fields=id,name,first_name,middle_name,last_name,'
                         'email,gender,locale,link,birthday,location,'
                         'relationship_status,website,about,age_range,'
                         'devices')

    def parse(self, data):
        parser_instance = parser.FacebookDataParser(data=data)
        return parser_instance.run()

    def save(self, data):
        try:
            user = User.objects.get(id=self.facebook_user.id)
        except User.DoesNotExist:
            message = "UserProfileEngine missing user for facebook_user %d"
            logger.warning(message % self.facebook_user.id)
        else:
            profile, created = (models.FacebookUserProfile.objects
                                .get_or_create(user=user, defaults=data))
            if not created:
                profile.update(data)
                profile.save()


class UserLikeEngine(BaseEngine):
    def fetch(self):
        graph = graph_api.get_graph_api(self.facebook_user)
        likes = []

        response = graph.get('me/likes', True)
        for page in response:
            if 'data' in page and page['data']:
                likes += page['data']
        return likes

    def parse(self, data):
        for like in data:
            like['id'] = int(like['id'])
            if 'created_time' in like:
                like['created_time'] = isodate.parse_datetime(
                    like['created_time'])
            else:
                like['created_time'] = timezone.now()
            yield like

    def get_user(self):
        try:
            return User.objects.get(id=self.facebook_user.id)
        except User.DoesNotExist:
            message = "UserProfileEngine missing user"
            logger.warning(message,
                           extra={'facebook_user': self.facebook_user.id})
            raise

    def save(self, data):
        user = self.get_user()
        processed_likes = []
        for like in data:
            user_like = models.FacebookUserLike.objects
            if 'name' in like:
                defaults = {'name': like['name'],
                            'category': like.get('category', 'undefined'),
                            'created_time': like['created_time']}

                like, _ = user_like.get_or_create(user=user,
                                                  facebook_id=like['id'],
                                                  defaults=defaults)
                processed_likes.append(like.id)
            else:
                logger.info('Like without a name', extra={'like': like})

        removed_likes = models.FacebookUserLike.objects.filter(user=user)
        removed_likes = removed_likes.exclude(id__in=processed_likes)
        removed_likes.delete()


class FacebookFriendEngine(BaseEngine):
    def fetch(self):
        graph = graph_api.get_graph_api(self.facebook_user)
        friends = []

        response = graph.get('me/friends', True)
        for page in response:
            if 'data' in page and page['data']:
                friends += page['data']
        return friends

    def parse(self, data):
        for friend in data:
            yield int(friend['id'])

    def save(self, data):
        user = self.get_user()
        processed_friends = []
        for friend_id in data:
            friend, _ = (models.FacebookFriend.objects
                         .get_or_create(user=user,
                                        friend_facebook_id=friend_id))
            processed_friends.append(friend.id)

        removed_friends = models.FacebookFriend.objects.filter(user=user)
        removed_friends = removed_friends.exclude(id__in=processed_friends)
        removed_friends.delete()

    def get_user(self):
        try:
            return User.objects.get(id=self.facebook_user.id)
        except User.DoesNotExist:
            message = "UserProfileEngine missing user for facebook_user %d"
            logger.warning(message % self.facebook_user.id)
            raise


ENGINES_ENABLED = [UserProfileEngine, UserLikeEngine, FacebookFriendEngine]
