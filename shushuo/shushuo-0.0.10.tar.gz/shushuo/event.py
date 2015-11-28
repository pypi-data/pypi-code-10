import re
import copy
from datetime import datetime
from shushuo import exceptions


Reserved_fields = [
    '@id',
    '@timestamp',
    '@location',
    '@actor',
]


class Event(object):
    """
    Event is the object used to validate and process event data before
    sending it to the Shushuo API
    """

    def __init__(self, collection_name, event_data):
        if not re.match('^[a-zA-Z_][a-zA-Z0-9_]*$', collection_name):
            raise exceptions.InvalidEventError(
                'Collection Name is not valid.')

        self.collection_name = collection_name

        self.body = self._process(event_data)

    def _process(self, event):
        """
        Checks if an event is valid for Shushuo and returns processed event
        that is safe to send to api.
        Raises InvalidEventError if the event is invalid

        :param event_data: dictionary with data for the event
        """
        if not isinstance(event, dict):
            raise exceptions.InvalidEventError('Event must be a dict object.')

        event_copy = copy.deepcopy(event)

        if '@timestamp' not in event_copy:
            event_copy['@timestamp'] = datetime.utcnow()

        if not isinstance(event_copy['@timestamp'], datetime):
            raise exceptions.InvalidEventError(
                'Timestamp must be a datetime object.')

        if '@id' in event_copy:
            raise exceptions.InvalidEventError('Event should not have id.')

        self._validate(event_copy)
        return event_copy

    def _validate(self, event, nested_depth=0):
        depth = nested_depth
        for key, value in event.items():
            if not isinstance(key, (str, unicode)):
                raise exceptions.InvalidEventError(
                    'Event key not valid %s' % key)
            elif nested_depth == 0 and key in Reserved_fields:
                pass
            elif not re.match('^[a-zA-Z][a-zA-Z0-9_]*$', key):
                if isinstance(key, unicode):
                    key = key.encode('utf-8')
                raise exceptions.InvalidEventError(
                    'Event key not valid %s' % key)

            if value is None:
                continue

            if isinstance(value, (unicode, str, long,
                                  int, float, bool)):
                continue
            elif isinstance(value, datetime):
                event[key] = value.isoformat()
            elif isinstance(value, dict):
                if key == '_location' and nested_depth == 0:
                    if len(value) == 2 and \
                       value.get('lat', None) and \
                       value.get('lon', None):
                        pass
                    else:
                        raise exceptions.InvalidEventError(
                            'invalid location format %s' % value)
                else:
                    _depth = self._validate(value,
                                            nested_depth=nested_depth+1)
                    depth = max(depth, _depth)
            elif isinstance(value, list):
                for item in value:
                    if not isinstance(item, (str, unicode)):
                        raise exceptions.InvalidEventError(
                            'invalid location format %s' % value)
            else:
                raise exceptions.InvalidEventError(
                    'unkown value type %s' % type(value))
        return depth
