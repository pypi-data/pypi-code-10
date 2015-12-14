#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : lhr (airhenry@gmail.com)
# @Link    : http://about.me/air.henry
from general import gs
log=gs.get_logger(__name__,debug=False)

import labkit.init_gs

import pymongo

from pymongo import MongoClient
client = MongoClient(host=gs.CONF.mongo_server, port=gs.CONF.mongo_port)
db=client['labkit']
context_collection=db['context']



def get_context():

    cursor=context_collection.find_one({'id':'context'})
    if not cursor:
        doc={'id':'context','context':{}}
        cursor=context_collection.insert_one(doc)

    context=cursor['context']
    return context

def update_context(conf):
    cursor=context_collection.find_one({'id':'context'})
    if not cursor:
        doc={'id':'context','context':{}}
        cursor=context_collection.insert_one(doc)

    context=cursor['context']
    context.update(conf)
    set_context(context)
    return 0

def set_context(context):

    cursor=context_collection.find_one({'id':'context'})
    if not cursor:
        doc={'id':'context','context':{}}
        cursor=context_collection.insert_one(doc)

    doc={'id':'context','context':context}
    context_collection.find_one_and_replace({'id':'context'},doc)


def test():
    pass


def run(conf):
    return True

def selfrun():
    import labkit.init_gs
    from general.interpreter.loader import callrun
    callrun(__file__)
if __name__ == '__main__':
    pass
    # set_context({})

    # test()
    # selfrun()





