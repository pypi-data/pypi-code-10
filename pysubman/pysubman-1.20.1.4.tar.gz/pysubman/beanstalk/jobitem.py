#!/usr/bin/env python
# coding=utf-8

import json
from collections import namedtuple
JobItem = namedtuple("_JobItem", ["topic", "status", "retry", "info"])


def encode(job_item):
    return json.dumps(dict(
        topic=job_item.topic,
        status=job_item.status,
        retry=job_item.retry,
        info=job_item.info
    ))


def decode(body):
    body_r = json.loads(body)
    return JobItem(
        topic=body_r["topic"],
        status=body_r["status"],
        retry=body_r["retry"],
        info=body_r["info"]
    )


def format(obj, *args):
    info = {}
    for index, k in enumerate(obj.Info):
        info[k[0]] = k[1] % (args[index])
    return info
