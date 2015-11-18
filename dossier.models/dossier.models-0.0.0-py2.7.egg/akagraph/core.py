'''AKAGraph core components

.. This software is released under an MIT/X11 open source license.
   Copyright 2015 Diffeo, Inc.
'''
from __future__ import absolute_import, division, print_function
import argparse
import gzip
import hashlib
from itertools import izip, imap
import logging
from operator import attrgetter, itemgetter
import sys
import time

import cbor
from elasticsearch import Elasticsearch, RequestError, NotFoundError
from elasticsearch.helpers import bulk, scan

logger = logging.getLogger(__name__)

RECORD_TYPE = 'record'
UNION_FIND_TYPE = 'union_find'

soft_selectors = ['name', 'username']
hard_selectors = ['email', 'phone', 'icq', 'skype', 'qq']

class AKAGraph(object):
    def __init__(self, hosts, index_name,
                 shards=20, buffer_size=100):
        self.conn = Elasticsearch(hosts=hosts, retry_on_timeout=True,
                                  max_retries=5)
        self.index = index_name
        self.shards = shards
        self.buffer_size = buffer_size
        self.buffer = []
        self.in_context = False

    def __enter__(self):
        self.in_context = True
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.in_context = False
        if exc_type is None and exc_value is None and traceback is None:
            self.flush()

    def add(self, rec):
        '''add `rec` to ES;  must be used inside a `with` statement
        '''
        assert self.in_context, 'must use "with" statement to add docs'
        self.buffer.append(rec)
        if len(self.buffer) >= self.buffer_size:
            self.flush()

    def flush(self):
        '''Actually do the work to ingest records gathered by calls to `add`.

        '''
        if not self.conn.indices.exists(index=self.index):
            self.create_index()
        logger.info('flushing ingest buffer (size: %d)', len(self.buffer))
        actions = []
        for rec in self.buffer:
            actions.append({
                '_index': self.index,
                '_type': RECORD_TYPE,
                '_id': rec['url'],
                '_op_type': 'index',
                '_source': rec
            })
        bulk(self.conn, actions, timeout=60, request_timeout=60)
        # next find equivalent records via exact match, and union them
        self.sync() # uh oh...

        count = 0
        for rec, equivs in self.find_equivs(self.buffer):
            count += 1
            equivs = set(equivs)
            if equivs:
                logger.info('found %d equivs for %r: %r', len(equivs), rec, equivs)
                equivs.add(rec['url'])
                self.unite(*equivs)
        self.buffer = self.buffer[:0]

    def sync(self):
        '''Forces data to disk, so that data from all calls to `put` will be
        available for getting and querying.  Generally, this should
        only be used in tests.

        '''
        self.conn.indices.refresh(index=self.index)

    def find_equivs(self, records):
        queries = []
        for rec in records:
            or_query = []
            for key, values in rec.iteritems():
                if key == 'url': continue
                if key in set(soft_selectors): continue
                if key not in set(hard_selectors): continue
                for v in values:
                    or_query.append({'term': {key: v,}})
            if len(or_query) == 0:
                raise Exception('trying to find equivs for record without '
                                'any hard selectors: %r', rec)

            query = {
                "query": {
                    "constant_score": {
                        "filter": {
                            "bool": {
                                "should": or_query,
                                "must_not": {"ids": {"values": [rec["url"]]}},
                            }
                        }
                    }
                }
            }
            #res = scan(self.conn, index=self.index, doc_type=RECORD_TYPE,
            #           _source_include=['_id'], query=query)
            #for resp in res:
            #    import pdb; pdb.set_trace()
            queries.append({'index': self.index, 'type': RECORD_TYPE, '_source_include': []})
            queries.append(query)

        # helper function for stripping down to just the URL
        def hits_generator(hits):
            for hit in hits['hits']['hits']:
                yield hit['_id']

        # now loop until we get answers for all the queries
        cursor = 0
        while queries:
            res = self.conn.msearch(body=queries)
            for hits in res['responses']:
                # remove the corresponding two rows of queries and corresponding record
                queries.pop(0); queries.pop(0)
                record = records[cursor]
                cursor += 1
                if 'error' in hits:
                    # need to run msearch again, starting with the query after the failed one
                    logger.warn("Error getting equivs for %s: %s", record, hits['error'])
                    break
                else:
                    yield (record, hits_generator(hits))

    def get_rec(self, url):
        '''get the record for `url`
        '''
        try:
            res = self.conn.get(index=self.index, doc_type=RECORD_TYPE, id=url)
            return res['_source']
        except NotFoundError:
            raise KeyError

    def find_equivs_by_selector(self, selector):
        or_query = []
        for key in hard_selectors:
            or_query.append({'term': {key: selector}})
        query = {
            "query": {
                "constant_score": {
                    "filter": {
                        "bool": {
                            "should": or_query,
                        }
                    }
                }
            }
        }
        res = self.conn.search(
            index=self.index, doc_type=RECORD_TYPE, 
            _source_include=[], body=query)
        '''
            body={
                'query': {
                    'multi_match': {
                        'query': selector,
                        'type': 'cross_fields',
                        # TODO: blend soft_selectors into this
                        'fields': hard_selectors,
                        }
                    }
                })
        '''
        for hit in res['hits']['hits']:
            logger.info(hit['_score'])
            yield self.root(hit['_id'])

    def find_connected_components(self, selector):
        equivs = set(self.find_equivs_by_selector(selector))
        # logger.warn(equivs)
        logger.info('get %d equivs for %r', len(equivs), selector)
        ccs = map(self.connected_component, equivs)
        def gen_cc(cc):
            for url in cc:
                yield self.get_rec(url)
        for cc in ccs:
            # logger.warn(cc)
            yield gen_cc(cc)

    def get_children(self, url):
        '''get child URLs of `url`
        '''
        res = scan(
            self.conn, index=self.index, doc_type=UNION_FIND_TYPE,
            _source_include=['child'],
            query={'query': {'term': {'parent': url}}})
        for item in res:
            yield item['_source']['child']

    def get_parent(self, url):
        '''get parent URL of `url`
        '''
        res = scan(
            self.conn, index=self.index, doc_type=UNION_FIND_TYPE,
            _source_include=['parent'],
            query={'query': {'term': {'child': url}}})
        for item in res:
            return item['_source']['parent']
        return url

    def get_all_unions(self):
        '''
        '''
        res = scan(
            self.conn, index=self.index, doc_type=UNION_FIND_TYPE)
        for item in res:
            yield item['_source']

    def set_parent(self, *pairs):
        '''set one or more `parent` URLs for `child` URLs by assembling a
        batch from `pairs`=[(`child`, `parent`), ...]

        '''
        actions = []
        for (child, parent) in pairs:
            actions.append({
                '_index': self.index,
                '_type': UNION_FIND_TYPE,
                '_id': child,
                '_op_type': 'index',
                '_source': {'parent': parent, 'child': child},
            })
        logger.info('set_parent bulk actions: %r', actions)
        bulk(self.conn, actions, timeout=60, request_timeout=60)

    def root(self, url):
        '''Find the root URL for `url`, which is itself it has not been united
        with anything.  A root `url` has itself as root.

        '''
        seen = set()
        while True:
            parent = self.get_parent(url)
            if parent == url: break
            if url in seen:
                logger.critical('hit loop: %r' % seen)
                sys.exit()
            seen.add(url)
            url = parent
        # TODO: do path compression here by setting parent to url for all in seen
        return url

    def find(self, url1, url2):
        return self.root(url1) == self.root(url2)

    def unite(self, *urls):
        roots = sorted({self.root(url) for url in urls})
        new_root = roots.pop(0)
        pairs = [(root, new_root) for root in roots]
        logger.info('%d pairs built for union', len(pairs))
        self.set_parent(*pairs)

    def connected_component(self, url):
        root = self.root(url)
        yield root
        stack = [root]
        while stack:
            root = stack.pop(0)
            for child in self.get_children(root):
                yield child
                stack.append(child)
        # do path compression here for all children

    def delete_index(self):
        try:
            self.conn.indices.delete(index=self.index)
        except NotFoundError:
            pass

    def create_index(self):
        try:
            self.conn.indices.create(index=self.index, body={
                'settings': {
                    # Once set, this can never change.
                    'number_of_shards': self.shards,
                    # ES recommends setting to 0 during ingest.
                    # (Because replicating documents is more work than
                    # replicating indexes.)
                    'number_of_replicas': 0,
                },
            })
        except RequestError:
            # Already exists.
            return

        properties = {'url': {
            'type': 'string',
            'index': 'not_analyzed',
        }}

        for soft_selector in soft_selectors:
            properties[soft_selector] = {
                'type': 'string',
                'index': 'analyzed',
            }
        for hard_selector in hard_selectors:
            properties[hard_selector] = {
                'type': 'string',
                'index': 'not_analyzed',
            }

        self.conn.indices.put_mapping(
            index=self.index, doc_type=RECORD_TYPE, body={
                RECORD_TYPE: {
                    '_all': {
                        'enabled': False,
                    },
                    'properties': properties
                },
            })

        self.conn.indices.put_mapping(
            index=self.index, doc_type=UNION_FIND_TYPE, body={
                UNION_FIND_TYPE: {
                    '_all': {
                        'enabled': False,
                    },
                    'properties': {
                        'parent': {
                            'type': 'string',
                            'index': 'not_analyzed',
                        },
                        'child': {
                            'type': 'string',
                            'index': 'not_analyzed',
                        },
                    },
                },
            })




def main():
    p = argparse.ArgumentParser('Ingest AKA records into ElasticSearch.')
    p.add_argument('--es-host', default='localhost:9200')
    p.add_argument('--es-index', default='akagraph')
    p.add_argument('--es-shards', default=20, type=int)
    p.add_argument('--buffer-size', default=100, type=int)
    p.add_argument('--delete', action='store_true', default=False)
    p.add_argument('--parent')
    p.add_argument('--ingest', nargs='+',
                   help='record files in gzipped CBOR format.')
    args = p.parse_args()

    logging.basicConfig(level=logging.INFO)

    aka = AKAGraph([args.es_host], args.es_index, 
                   buffer_size=args.buffer_size,
                   shards=args.es_shards)

    if args.delete:
        aka.delete_index()
        sys.exit()

    if args.parent:
        print(aka.get_parent(unicode(args.parent)))
        sys.exit()

    if args.ingest:
        total = 0
        skipped = 0
        start = time.time()
        with aka:
            for rec_path in args.ingest:
                fopen = open
                if rec_path.endswith('.gz'):
                    fopen = gzip.open
                logger.info('loading %r', rec_path)
                with fopen(rec_path) as fdoc:
                    while True:
                        try:
                            rec = cbor.load(fdoc)
                        except EOFError:
                            break
                        rec = {key.lower(): val for key, val in rec.items()}
                        aka.add(rec)
                        total += 1
                        if total % 1000 == 0:
                            elapsed = time.time() - start
                            rate = total / elapsed
                            logger.info('%d done in %.1f sec --> %.1f per sec', 
                                        total, elapsed, rate)
                logger.info('finished %s, total recs=%d' % (rec_path, total))
        logger.info('finished %d recs' % total)

if __name__ == '__main__':
    main()
