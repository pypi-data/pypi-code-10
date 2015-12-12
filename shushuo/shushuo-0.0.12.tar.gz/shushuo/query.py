import re
import copy
from shushuo import exceptions

Reserved_aggregations = [
    'max',
    'min',
    'avg',
    'sum',
    'count',
    'unique',
    'last',
]

Reserved_timeframes = [
    'this_minute',
    'last_minute',
    'this_hour',
    'last_hour',
    'today',
    'yesterday',
    'this_week',
    'last_week',
    'this_month',
    'last_month',
    'this_year',
    'last_year'
]

Reserved_intervals = [
    'minute',
    'hour',
    'day',
    'week',
    'month',
    'year',
]

Reserved_fields = [
    'select',
    'filter',
    'interval',
    'group_by',
    'timeframe',
    'timezone',
]


class Query(object):
    """
    Query is the object used to validate and process event data before
    sending it to the Shushuo API
    """

    def __init__(self, collection_name, query_data):
        if not re.match('^[a-zA-Z_][a-zA-Z0-9_]*$', collection_name):
            raise exceptions.InvalidEventError(
                'Collection Name is not valid.')

        self.collection_name = collection_name
        self.body = self._process(query_data)

    def _process(self, query):
        if not isinstance(query, dict):
            raise exceptions.InvalidQueryError('Query must be a dict object.')

        unknow_keys = set(query.keys()) - set(Reserved_fields)
        if unknow_keys:
            raise exceptions.InvalidQueryError(
                'Query should not contain %s.' % unknow_keys)

        if 'select' not in query:
            raise exceptions.InvalidQueryError(
                'Query should atleast contain select.')

        query_copy = copy.deepcopy(query)

        for field in query_copy:
            query_copy[field] = getattr(self, '_process_%s' % field)(
                query_copy.get(field, None)
            )

        return query_copy

    def _process_select(self, select):
        if select == '*':
            select = ['*']

        if select == 'count(*)':
            select = {
                'count': 'count'
            }

        if isinstance(select, dict):
            for label in select:
                aggregate = select[label]
                if aggregate == 'count':
                    continue

                if isinstance(aggregate, dict) and len(aggregate.keys()) == 1:
                    aggregation, field = aggregate.items()[0]
                    if aggregation not in Reserved_aggregations:
                        raise exceptions.InvalidQueryError(
                            'Unknown aggregation %s.' % aggregation)
                    if not isinstance(field, (str, unicode)):
                        raise exceptions.InvalidQueryError(
                            'Query field %s should be string.' % field)
                else:
                    raise exceptions.InvalidQueryError(
                        'Invalid Aggregate format %s.' % aggregate)
        elif isinstance(select, list):
            if len(select) == 0:
                raise exceptions.InvalidQueryError(
                    'Select should not be empty.')
            for field in select:
                if not isinstance(field, (str, unicode)):
                    raise exceptions.InvalidQueryError(
                        'Query field %s should be string.' % field)
        else:
            raise exceptions.InvalidQueryError(
                'Select format should be list or dictionary.')

        return select

    def _process_timezone(self, timezone):
        if timezone is None:
            return timezone

        if not isinstance(timezone, int):
            raise exceptions.InvalidQueryError(
                'Timezone field %s should be int.' % timezone)
        return timezone

    def _process_timeframe(self, timeframe):
        if timeframe is None:
            return timeframe

        if isinstance(timeframe, str):
            if timeframe not in Reserved_timeframes:
                raise exceptions.InvalidQueryError(
                    'Unkonw timeframe value %s.' % timeframe)
        elif isinstance(timeframe, dict):
            pass
        else:
            raise exceptions.InvalidQueryError(
                'Unkonw Timeframe format %s.' % timeframe)

        return timeframe

    def _process_interval(self, interval):
        if interval is None:
            return interval

        if interval not in Reserved_intervals:
            raise exceptions.InvalidQueryError(
                'Unkonw Interval value %s.' % interval)
        return interval

    def _process_filter(self, _filter):
        return _filter

    def _process_group_by(self, group_by):
        if group_by is None:
            return group_by

        if not isinstance(group_by, str):
            raise exceptions.InvalidQueryError(
                'GroupBy field %s should be string.' % group_by)
        return group_by
