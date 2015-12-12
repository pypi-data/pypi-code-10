from collections import defaultdict
from shushuo.api import ShushuoApi
from shushuo.event import Event
from shushuo.profile import Profile
from shushuo.query import Query
from shushuo import exceptions


class ShuClient(object):

    def __init__(self, project_id, project_key, endpoint_url=None,
                 api_class=ShushuoApi, get_timeout=60, post_timeout=10):
        super(ShuClient, self).__init__()

        # Set up an api client to be used for querying and optionally passed
        # into a default persistence strategy.
        self.api = api_class(project_id, project_key,
                             endpoint_url=endpoint_url,
                             get_timeout=get_timeout,
                             post_timeout=post_timeout)

        self.project_id = project_id

    def push_event(self, collection, event_body):
        event = Event(collection, event_body)
        return self.api.post_event(event.collection_name,
                                   event.body)

    def push_events(self, events):
        if not isinstance(events, (dict)):
            raise exceptions.InvalidEventError(
                "Events must be a list of dict objects")

        events_by_collection = defaultdict(list)
        for collection in events:
            if isinstance(events[collection], list):
                for event in events[collection]:
                    e = Event(collection, event)
                    events_by_collection[collection].append(e.body)
            else:
                raise exceptions.InvalidEventError(
                    "Events must be a list of dict objects")

        return self.api.post_events(events_by_collection)

    def query_events(self, collection, query_body):
        query = Query(collection, query_body)

        return self.api.query_events(query.collection_name,
                                     query.body)

    query = query_events
    push = push_event
    mpush = push_events

    def update_profile(self, collection, profile_body):
        profile = Profile(collection, profile_body)
        return self.api.post_profile(profile.collection_name,
                                     profile.body)
