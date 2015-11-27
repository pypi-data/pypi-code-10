#-*- coding: utf-8 -*-

from pymongo import MongoClient

__all__ = ['get_client']


DEFAULT_PORT = 27017


def get_client(db_name, host, port=DEFAULT_PORT):
    return MongoClient(host, port)[db_name]
