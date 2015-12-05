# -*- coding: utf-8 -*-
def associate_by_user_id(backend, details, response, user=None, *args, **kwargs):
    """
    Associate current auth with a user with the same Google user_id in the DB.
    """
    if user:
        return None

    user_id = response.get('id')
    if user_id:
        # Try to associate accounts registered with the same Google user_id.
        for provider in ('google-appengine-oauth', 'google-appengine-oauth2'):
            social = backend.strategy.storage.user.get_social_auth(provider, user_id)
            if social:
                user = social.user
                if user:
                    return {'user': user}
