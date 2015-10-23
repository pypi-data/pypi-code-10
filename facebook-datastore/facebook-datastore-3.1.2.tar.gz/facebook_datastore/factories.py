import factory

from facebook_auth import models


class FacebookUserFactory(factory.DjangoModelFactory):
    FACTORY_FOR = models.FacebookUser

    user_id = factory.Sequence(lambda n: n)
