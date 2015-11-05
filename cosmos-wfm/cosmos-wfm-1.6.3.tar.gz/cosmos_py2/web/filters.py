from __future__ import division
from __future__ import absolute_import
import datetime, re
from .. import StageStatus, TaskStatus
from flask import Markup
from sqlalchemy import func
from cosmos.api import Task, Stage, Execution


def add_filters(bprint_or_app, type_=u'bprint'):
    add_filter = bprint_or_app.add_app_template_filter if type_ == u'bprint' else bprint_or_app.add_template_filter

    @add_filter
    def to_thumb(b):
        if b:
            s = u'<span class="glyphicon glyphicon-thumbs-up"></span> yes'
        else:
            s = u'<span class="glyphicon glyphicon-thumbs-down"></span> no'
        return Markup(s)


    @add_filter
    def format_resource_usage(field_name, val):
        if val is None:
            return u''
        if re.search(ur"time", field_name):
            return u"{1}".format(val, format_time(val))
        elif field_name == u'percent_cpu':
            return u"{0}%".format(val*100)
        elif u'mem' in field_name:
            return format_memory_kb(val)
        elif type(val) in [int, int]:
            return intWithCommas(val)
        return unicode(val)

    @add_filter
    def stage_status2bootstrap(status):
        d = {
            StageStatus.no_attempt: u'info',
            StageStatus.running: u'warning',
            StageStatus.successful: u'success',
            StageStatus.failed: u'failure',
            StageStatus.killed: u'failure'
        }
        return d.get(status)

    @add_filter
    def or_datetime_now(x):
        return x or datetime.datetime.now()


    @add_filter
    def stage_stat(stage, attribute, func_name):
        f = getattr(func, func_name)
        session = stage.session
        a = session.query(f(getattr(Task, attribute))).join(Stage).filter(Stage.id == stage.id).scalar()
        if a is None:
            return u''
        a = int(a)
        if u'rss' in attribute:
            return format_memory_kb(a)
        if u'mem_req' in attribute:
            return format_memory_mb(a)
        if u'time' in attribute:
            return format_time(a)
        if u'percent' in attribute:
            return u'{}%'.format(a)
        return a

    @add_filter
    def datetime_format(value, format=u'%Y-%m-%d %H:%M'):
        return value.strftime(format) if value else u'None'

    @add_filter
    def parse_seconds(amount, type=u"seconds"):
        if amount is None or amount == u'':
            return u''
        if type == u'minutes':
            amount = amount * 60
        amount = int(amount) if amount > 5 else amount
        return datetime.timedelta(seconds=amount)

def intWithCommas(x):
    if x is None:
        return u''
    if type(x) not in [type(0), type(0)]:
        #raise TypeError("Parameter must be an integer.")
        return x
    if x < 0:
        return u'-' + intWithCommas(-x)
    result = u''
    while x >= 1000:
        x, r = divmod(x, 1000)
        result = u",%03d%s" % (r, result)
    return u"%d%s" % (x, result)


def format_memory_kb(kb):
    u"""converts kb to human readible"""
    if kb is None:
        return u''
    mb = kb / 1024.0
    gb = mb / 1024.0
    if gb > 1:
        return u"%sGB" % round(gb, 1)
    else:
        return u"%sMB" % round(mb, 1)

def format_memory_bytes(str):
    return format_memory_kb(str/1024)

def format_memory_mb(mb):
    u"""converts mb to human readible"""
    return format_memory_kb(mb * 1024.0) if mb else u""


def format_time(amount, type=u"seconds"):
    if amount is None or amount == u'':
        return u''
    if type == u'minutes':
        amount = amount * 60
    return datetime.timedelta(seconds=int(amount))