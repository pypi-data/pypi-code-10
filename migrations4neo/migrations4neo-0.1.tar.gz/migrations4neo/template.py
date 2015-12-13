body = '''# -*- coding: utf-8 -*-
import os

from py2neo import Graph

graph = Graph(os.getenv('NEO4J_REST_URL'))
cypher = graph.cypher


# MIGRATION: {}


def up():
    cypher.execute(""" """)


def down():
    cypher.execute(""" """)
'''
