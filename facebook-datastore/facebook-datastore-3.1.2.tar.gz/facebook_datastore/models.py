import logging

from django.db import models


logger = logging.getLogger(__name__)


class FacebookUserProfileManager(models.Manager):
    def create_or_update(self, parameters):
        """Parameters must include 'facebook_id' key."""
        try:
            instance = self.get(facebook_id=parameters['facebook_id'])
        except FacebookUserProfile.DoesNotExist:
            return FacebookUserProfile(**parameters)
        instance.update(parameters)
        return instance


class FacebookUserProfile(models.Model):
    GENDERS = (
        ('m', 'Male'),
        ('f', 'Female'),
    )

    user = models.OneToOneField('auth.User')

    facebook_id = models.BigIntegerField(unique=True)
    access_token = models.TextField(null=True, blank=True)

    name = models.TextField(null=True, blank=True)
    first_name = models.TextField(null=True, blank=True)
    last_name = models.TextField(null=True, blank=True)
    middle_name = models.TextField(null=True, blank=True)
    username = models.TextField(null=True, blank=True)
    email = models.EmailField(null=True, blank=True, max_length=254)

    gender = models.CharField(max_length=1, choices=GENDERS, null=True,
                              blank=True)
    locale = models.CharField(max_length=5, null=True, blank=True)
    link = models.URLField(null=True, blank=True)
    birthday = models.DateField(null=True, blank=True,
                                help_text='needs user_birthday')
    location_name = models.TextField(null=True, blank=True,
                                     help_text='needs user_location')
    location_id = models.TextField(null=True, blank=True,
                                   help_text='needs user_location')
    relationship_status = models.TextField(
        null=True, blank=True, help_text='needs user_relationship'
    )
    website = models.TextField(null=True, blank=True,
                               help_text='needs user_website')
    about_me = models.TextField(blank=True, null=True,
                                help_text='needs user_about_me')
    raw_data = models.TextField(blank=True, null=True)
    age_range_min = models.IntegerField(blank=True, null=True)
    age_range_max = models.IntegerField(blank=True, null=True)
    uses_ios = models.BooleanField(default=False)
    uses_android = models.BooleanField(default=False)

    objects = FacebookUserProfileManager()

    def update(self, parameters):
        for key, value in parameters.items():
            if hasattr(self, key):
                setattr(self, key, value)
            else:
                logger.warning("FacebookUserProfile has no '%s' attribute"
                               % key)


class FacebookUserLike(models.Model):
    user = models.ForeignKey('auth.User')
    name = models.TextField()
    category = models.CharField(max_length=250)
    facebook_id = models.BigIntegerField()
    created_time = models.DateTimeField()

    class Meta:
        unique_together = ("user", "facebook_id")


class FacebookFriend(models.Model):
    user = models.ForeignKey('auth.User')
    friend_facebook_id = models.BigIntegerField()

    class Meta:
        unique_together = (('user', 'friend_facebook_id'),)
