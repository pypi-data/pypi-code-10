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


class ReducedReportMixin:

    """Mixin for reports that use map reduce."""

    map_reduce_js_file = None
    # The collection to be reduced.
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

    @classmethod
    def get_js(cls):
        """Returns the content of the js file"""

        fname = os.path.join(HERE, cls.map_reduce_js_file)
        with open(fname, 'r') as fd:
            contents = fd.read()

        return contents

    @classmethod
    def get_mapf(cls):
        """Returns the map function defined at ``cls.map_reduce_js_file``.
        The map function is enclosed by the js comments
        ``// map function`` and ``// end map function``. These comments
        are used to retrieve the function from the js file.
        """

        js = cls.get_js()
        pat = re.compile('//\s*map function(.*?)//\s*end map function',
                         re.MULTILINE | re.DOTALL | re.UNICODE)
        mapf = re.findall(pat, js)[0].replace('mapf =', '').strip()
        return mapf

    @classmethod
    def get_reducef(cls):
        """Returns the reduce function defined at ``cls.map_reduce_js_file``.
        The reduce function is enclosed by the js comments
        ``// reduce function`` and ``// end reduce function``. These comments
        are used to retrieve the function from the js file.
        """

        js = cls.get_js()
        pat = re.compile('//\s*reduce function(.*?)//\s*end reduce function',
                         re.MULTILINE | re.DOTALL | re.UNICODE)
        reducef = re.findall(pat, js)[0].replace('reducef =', '').strip()
        return reducef

    @classmethod
    def get_finalizef(cls):
        """Returns the finalize function defined at ``cls.map_reduce_js_file``.
        The finalize function is enclosed by the js comments
        ``// finalize function`` and ``// end finalize function``. These
        comments are used to retrieve the function from the js file.
        """

        js = cls.get_js()
        pat = re.compile('//\s*finalize function(.*?)//\s*end finalize function',
                         re.MULTILINE | re.DOTALL | re.UNICODE)
        result = re.findall(pat, js)
        if not result:
            return None

        finalizef = result[0].replace('finalizef =', '').strip()
        return finalizef

    @classmethod
    @gen.coroutine
    def do_map_reduce(cls, **kwargs):
        """Executes a map-reduce over ``cls.base_collection`` and merges
        it to ``cls._collection_name``.
        """

        mapf = cls.get_mapf()
        reducef = cls.get_reducef()
        finalizef = cls.get_finalizef()
        qs = cls.base_collection.objects.filter(**kwargs)
        kw = {}
        if finalizef:
            kw = {'finalize_f': finalizef}

        collection_name = cls._get_collection_name()
        r = yield qs.map_reduce(mapf, reducef, {'merge': collection_name},
                                **kw)
        return r


class ThemeReportMixin(ReducedReportMixin):

    """A Mixin for reports related to themes"""

    @classmethod
    @gen.coroutine
    def get_themes_report(cls, **kwargs):
        """Returns the consolidated data for themes reports.

        :param kwargs: Arguments to filter the queryset before
          aggregating it."""

        kw = super()._format_kw(**kwargs)

        group = {"$group":
                 {'_id': '$_id.theme',
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
                 {'_id': {'theme': '$_id.theme',
                          'date': '$_id.date'},
                  'total': {'$sum': '$value'}}}

        r = yield cls.objects.filter(**kw).aggregate(group)

        return super()._format_history_result('theme', r)


class SiteReportMixin(ReducedReportMixin):

    """A Mixin for reports related to sites."""

    @classmethod
    @gen.coroutine
    def get_sites_report(cls, **kwargs):
        """Returns the consolidated data for sites reports.

        :param kwargs: Arguments to filter the queryset before
          aggregating it."""

        kw = super()._format_kw(**kwargs)

        group = {"$group":
                 {'_id': '$_id.site',
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
                 {'_id': {'site': '$_id.site',
                          'date': '$_id.date'},
                  'total': {'$sum': '$value'}}}

        r = yield cls.objects.filter(**kw).aggregate(group)

        return super()._format_history_result('site', r)


class ContentReportMixin(ReducedReportMixin):

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


class ThemeConsumption(MapReduceDocument, ThemeReportMixin):

    """ This Document is the result of a map-reduce done in the
    content_consumption collection. It reduces the consumption to
    a consolidated consumption by theme/site/day.

    """

    map_reduce_js_file = os.path.join('js', 'theme_consumption.js')


class SiteConsumption(MapReduceDocument, SiteReportMixin):

    """ This Document is the result of a map-reduce done in the
    content_consumption collection. It reduces the consumption to
    a consolidated consumption by site/day.
    """

    map_reduce_js_file = os.path.join('js', 'site_consumption.js')


class ThemeConsumers(MapReduceDocument, ThemeReportMixin):

    """ This Document is the result of a map-reduce done in the
    content_consumption collection. It reduces the consumption to
    consolidated consumers by theme/day.
    """

    map_reduce_js_file = os.path.join('js', 'theme_consumers.js')


class SiteConsumers(MapReduceDocument, SiteReportMixin):

    """ This Document is the result of a map-reduce done in the
    content_consumption collection. It reduces the consumption to
    consolidated consumers by site/day.
    """

    map_reduce_js_file = os.path.join('js', 'site_consumers.js')


class ContentConsumptionReport(MapReduceDocument, ContentReportMixin):

    """ This Document is the result of a map-reduce done in the
    content_consumption collection. It reduces the consumption to
    consolidated consumption by content/day."""

    map_reduce_js_file = os.path.join('js', 'content_consumption.js')


class ContentConsumersReport(MapReduceDocument, ContentReportMixin):

    """ This Document is the result of a map-reduce done in the
    content_consumption collection. It reduces the consumption to
    consolidated consumers by content/day."""

    map_reduce_js_file = os.path.join('js', 'content_consumers.js')


class IncrementalMapReduce(Document):

    """This class takes care of incrementally execute the map
    reduce for the reduced reports."""

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
            future = reduced_cls.do_map_reduce(**kw)
            yield cls._set_since_for(coll_name)
            futures.append(future)
        return futures

    @classmethod
    @gen.coroutine
    def do_today_map_reduce(cls):
        """Do map reduce for the current day."""

        futures = []
        now = datetime.datetime.now()
        today = datetime.datetime(now.year, now.month, now.day)
        for reduced_cls in cls._reduced:
            future = reduced_cls.do_map_reduce(inclusion_date__gte=today)
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
        for reduced_cls in cls._reduced:
            future = reduced_cls.do_map_reduce(inclusion_date__gte=yesterday,
                                               inclusion_date__lt=today)
            futures.append(future)

        return futures


if hasattr(settings, 'USE_REDUCED_REPORTS') and settings.USE_REDUCED_REPORTS:
    reduced_reports = [SiteThemeConsumption, SiteConsumers, ThemeConsumers,
                       ContentConsumersReport, ContentConsumptionReport]
    for r in reduced_reports:
        IncrementalMapReduce.add(r)

    # 2 hours
    secs = 3600 * 2
    print('adding incremental daily map reduce to scheduler')
    scheduler.add(IncrementalMapReduce.do_today_map_reduce, secs)
    scheduler.add(IncrementalMapReduce.do_yesterday_map_reduce,
                  hour_min=(0, 0))
