# -*- coding: utf-8 -*-

# In this module is the consolidated data for reports about
# Jaobi usage.

import os
import re
from collections import defaultdict
import datetime
from mongomotor.document import Document, MapReduceDocument
from mongomotor.fields import StringField, DateTimeField
from pyrocumulus.conf import settings
from tornado import gen
from jaobi import models
from jaobi.scheduler import scheduler

HERE = os.path.abspath(os.path.dirname(__file__))


class ReportMixin:

    """Base mixin for reports"""

    base_collection = models.ContentConsumption

    @classmethod
    def _format_kw(cls, **kwargs):
        kw = {}
        for k, v in kwargs.items():
            if not k.startswith('id__'):
                k = 'id__{}'.format(k)
            kw[k] = v
        return kw

    @classmethod
    def _format_result(cls, result):

        results = result['result']
        rdict = {}
        for r in results:
            rdict[r['_id']] = r['total']
        return rdict

    @classmethod
    def _format_history_result(cls, key, result):
        rdict = defaultdict(list)
        for r in result['result']:
            rdict[r['_id'][key]].append({'date': r['_id']['date'],
                                         'total': r['total']})

        for k, v in rdict.items():
            rdict[k] = sorted(v, key=lambda d: d['date'], reverse=True)

        return rdict


class AggregatedReportMixin(ReportMixin):

    """Mixin for reports that use aggregation"""

    aggregation_fields = {}

    @classmethod
    def get_dated_project(cls):
        """Returns a list representing the two first steps of a
        pipeline for grouping this by day.
        """

        pipeline = [
            {'$project': dict(date='$inclusion_date',
                              h={'$hour': '$inclusion_date'},
                              m={'$minute': '$inclusion_date'},
                              s={'$second': '$inclusion_date'},
                              ms={'$millisecond': '$inclusion_date'},
                              **cls.aggregation_fields)},
            {'$project': dict(date={'$subtract':
                                    ['$date',
                                     {'$add': ['$ms',
                                               {'$multiply': ['$s', 1000]},
                                               {'$multiply': ['$m', 60, 1000]},
                                               {'$multiply': ['$h',
                                                              3600, 1000]}]}]},
                              **cls.aggregation_fields)}]
        return pipeline

    @classmethod
    def get_out_step(cls):
        """Returns the step for sending the result of an aggregation
        to a collection. It must be the last step in a pipeline."""

        return {'$out': cls._get_collection_name()}

    @classmethod
    def get_pipeline(cls):
        """Returns the pipeline for aggregation. Must be implemented in
        subclasses."""
        raise NotImplementedError

    @classmethod
    @gen.coroutine
    def do_aggregate(cls, **kwargs):
        """Aggregates ``cls.base_collection`` to count consumers by
        field.

        :param kwargs: Filter to queryset.
        """

        qs = cls.base_collection.objects.filter(**kwargs)
        pipeline = cls.get_pipeline()
        r = yield qs.aggregate(*pipeline)
        return r


class ConsumptionReportMixin(AggregatedReportMixin):

    """Mixin for reports related to consumption."""

    @classmethod
    def get_pipeline(cls):
        """Returns the pipeline for consumption aggregation."""

        pipeline = super().get_dated_project()

        d = cls.aggregation_fields.copy()
        d.update({'date': '$date'})
        group = {'$group': {'_id': d, 'value': {'$sum': 1}}}
        pipeline.append(group)
        pipeline.append(cls.get_out_step())
        return pipeline


class ConsumerReportMixin(AggregatedReportMixin):

    """Mixin for reports related to consumers."""

    @classmethod
    def get_pipeline(cls):
        """Returns the pipeline for consumers aggretation."""

        d = cls.aggregation_fields.copy()
        cls.aggregation_fields.update({'consumer': '$consumer'})
        pipeline = super().get_dated_project()

        d = cls.aggregation_fields.copy()
        d.update({'date': '$date'})
        # Here we group unique consumers by key/day
        group = {'$group': {'_id': d, 'consumers': {'$addToSet': '$consumer'}}}
        pipeline.append(group)
        # Here we have the count of consumers
        project = {'$project': {'_id': '$_id',
                                'value': {'$size': '$consumers'}}}
        pipeline.append(project)
        # And here we direct the output to a collection
        pipeline.append(cls.get_out_step())
        return pipeline


class ThemeReportMixin(ReportMixin):

    """A Mixin for reports related to themes"""

    @classmethod
    def get_pipeline(cls):
        """Returns a pipeline with themes unwinded."""

        pipeline = super().get_pipeline()
        # unwind themes before aggregation so we count
        # consumers by theme.
        pipeline.insert(2, {'$unwind': '$themes'})
        return pipeline

    @classmethod
    @gen.coroutine
    def get_themes_report(cls, **kwargs):
        """Returns the consolidated data for themes reports.

        :param kwargs: Arguments to filter the queryset before
          aggregating it."""

        kw = super()._format_kw(**kwargs)

        group = {"$group":
                 {'_id': '$_id.themes',
                  'total': {'$sum': '$value'}}}

        r = yield cls.objects.filter(**kw).aggregate(group)

        return super()._format_result(r)

    @classmethod
    @gen.coroutine
    def get_themes_report_history(cls, **kwargs):
        """Returns the history data for themes reports.

        :param kwargs: Arguments to filter the queryset before
          aggregating it."""

        kw = super()._format_kw(**kwargs)

        group = {'$group':
                 {'_id': {'theme': '$_id.themes',
                          'date': '$_id.date'},
                  'total': {'$sum': '$value'}}}

        r = yield cls.objects.filter(**kw).aggregate(group)

        return super()._format_history_result('theme', r)


class SiteReportMixin(ReportMixin):

    """A Mixin for reports related to sites."""

    @classmethod
    @gen.coroutine
    def get_sites_report(cls, **kwargs):
        """Returns the consolidated data for sites reports.

        :param kwargs: Arguments to filter the queryset before
          aggregating it."""

        kw = super()._format_kw(**kwargs)

        group = {"$group":
                 {'_id': '$_id.origin',
                  'total': {'$sum': '$value'}}}

        r = yield cls.objects.filter(**kw).aggregate(group)

        return super()._format_result(r)

    @classmethod
    @gen.coroutine
    def get_sites_report_history(cls, **kwargs):
        """Returns the history data for sites reports.

        :param kwargs: Arguments to filter the queryset before
          aggregating it."""

        kw = super()._format_kw(**kwargs)

        group = {'$group':
                 {'_id': {'origin': '$_id.origin',
                          'date': '$_id.date'},
                  'total': {'$sum': '$value'}}}

        r = yield cls.objects.filter(**kw).aggregate(group)
        return super()._format_history_result('origin', r)


class ContentReportMixin(ReportMixin):

    """ Mixin for reports related to content."""

    @classmethod
    @gen.coroutine
    def _format_content_result(cls, result):
        rdict = {}
        contents = [r['_id'] for r in result['result']]
        contents = yield models.Content.objects.filter(
            id__in=contents).to_list()

        def get_result(rid):
            for c in result['result']:
                if c['_id'] == rid:
                    return c['total']

        for i, c in enumerate(contents):
            rdict[c] = get_result(c.id)

        return rdict

    @classmethod
    @gen.coroutine
    def get_content_report(cls, limit=None, **kwargs):
        """Returns the consolidated data for content reports.

        :param limit: Limit for aggregation results.
        :param kwargs: Arguments to filter the queryset before
          aggregating it."""

        kw = super()._format_kw(**kwargs)

        group = {'$group':
                 {'_id': '$_id.content',
                  'total': {'$sum': '$value'}}}
        pipeline = [group]
        if limit:
            limit = {'$limit': limit}
            pipeline.append(limit)

        r = yield cls.objects.filter(**kw).aggregate(*pipeline)
        formated = yield cls._format_content_result(r)
        return formated


class ThemeConsumption(MapReduceDocument, ThemeReportMixin,
                       ConsumptionReportMixin):

    """ This Document is the result of a map-reduce done in the
    content_consumption collection. It reduces the consumption to
    a consolidated consumption by theme/site/day.

    """

    aggregation_fields = {'origin': '$origin',
                          'themes': '$themes'}


class SiteConsumption(MapReduceDocument, SiteReportMixin,
                      ConsumptionReportMixin):

    """ This Document is the result of an aggregation done in the
    content_consumption collection. It reduces the consumption to
    a consolidated consumption by site/day.
    """

    aggregation_fields = {'origin': '$origin'}


class ThemeConsumers(MapReduceDocument, ThemeReportMixin, ConsumerReportMixin):

    """ This Document is the result of an aggregation done in the
    content_consumption collection. It reduces the consumption to
    consolidated consumers by theme/day.
    """

    aggregation_fields = {'themes': '$themes'}


class SiteConsumers(MapReduceDocument, SiteReportMixin, ConsumerReportMixin):

    """ This Document is the result of an aggregation done in the
    content_consumption collection. It reduces the consumption to
    consolidated consumers by site/day.
    """

    aggregation_fields = {'origin': '$origin'}


class ContentConsumptionReport(MapReduceDocument, ContentReportMixin,
                               ConsumptionReportMixin):

    """ This Document is the result of an aggregation done in the
    content_consumption collection. It reduces the consumption to
    consolidated consumption by content/day."""

    aggregation_fields = {'content': '$content'}


class ContentConsumersReport(MapReduceDocument, ContentReportMixin,
                             ConsumerReportMixin):

    """ This Document is the result of an aggretation done in the
    content_consumption collection. It reduces the consumption to
    consolidated consumers by content/day."""

    aggregation_fields = {'content': '$content'}


class IncrementalMapReduce(Document):

    """This class takes care of incrementally execute the map
    reduce (or aggretation) for reports."""

    collection = StringField(unique=True, required=True)
    last_incr = DateTimeField()
    _reduced = []

    @classmethod
    @gen.coroutine
    def _get_since_for(cls, collection_name):
        try:
            col_incr = yield cls.objects.get(collection=collection_name)
        except cls.DoesNotExist:
            col_incr = cls(collection=collection_name)
            yield col_incr.save()

        begin_of_all_times = settings.BEGIN_OF_ALL_TIMES if hasattr(
            settings, 'BEGIN_OF_ALL_TIMES') else None

        since = col_incr.last_incr or begin_of_all_times
        return since

    @classmethod
    @gen.coroutine
    def _set_since_for(cls, collection_name):
        col_incr = yield cls.objects.get(collection=collection_name)
        col_incr.last_incr = datetime.datetime.now()
        yield col_incr.save()

    @classmethod
    def add(cls, reduced_cls):
        """Adds a reduced report to the map-reduce queue."""

        cls._reduced.append(reduced_cls)

    @classmethod
    @gen.coroutine
    def do_incremental_map_reduce(cls):
        """Do an incremental map reduce since the last time
        it was done."""

        futures = []
        for reduced_cls in cls._reduced:
            kw = {}
            coll_name = reduced_cls._get_collection_name()
            since = yield cls._get_since_for(coll_name)
            if since:
                kw = {'inclusion_date__gte': since}

            if hasattr(reduced_cls, 'do_map_reduce'):
                future = reduced_cls.do_map_reduce(**kw)
                futures.append(future)

            if hasattr(reduced_cls, 'do_aggregate'):
                future = reduced_cls.do_aggregate(**kw)
                futures.append(future)

            yield cls._set_since_for(coll_name)
        return futures

    @classmethod
    @gen.coroutine
    def do_today_map_reduce(cls):
        """Do map reduce for the current day."""

        futures = []
        now = datetime.datetime.now()
        today = datetime.datetime(now.year, now.month, now.day)
        kw = {'inclusion_date__gte': today}
        for reduced_cls in cls._reduced:
            if hasattr(reduced_cls, 'do_map_reduce'):
                future = reduced_cls.do_map_reduce(**kw)
                futures.append(future)

            if hasattr(reduced_cls, 'do_aggregate'):
                future = reduced_cls.do_aggregate(**kw)
                futures.append(future)

        return futures

    @classmethod
    @gen.coroutine
    def do_yesterday_map_reduce(cls):
        """Do map reduce for the last day."""

        futures = []
        now = datetime.datetime.now()
        today = datetime.datetime(now.year, now.month, now.day)
        yesterday = today - datetime.timedelta(days=1)

        kw = {'inclusion_date__gte': yesterday,
              'inclusion_date__lt': today}
        for reduced_cls in cls._reduced:
            if hasattr(reduced_cls, 'do_map_reduce'):
                future = reduced_cls.do_map_reduce(**kw)
                futures.append(future)

            if hasattr(reduced_cls, 'do_aggregate'):
                future = reduced_cls.do_aggregate(**kw)
                futures.append(future)

        return futures


if hasattr(settings, 'USE_REDUCED_REPORTS') and settings.USE_REDUCED_REPORTS:
    reduced_reports = [ThemeConsumption, SiteConsumption,
                       SiteConsumers, ThemeConsumers, ContentConsumersReport,
                       ContentConsumptionReport]
    for r in reduced_reports:
        IncrementalMapReduce.add(r)

    # 2 hours
    secs = 3600 * 2
    print('adding incremental daily map reduce to scheduler')
    scheduler.add(IncrementalMapReduce.do_today_map_reduce, secs)
    scheduler.add(IncrementalMapReduce.do_yesterday_map_reduce,
                  hour_min=(0, 0))
