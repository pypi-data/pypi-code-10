import logging

from collections import defaultdict, Counter
from time import sleep, time
logging.basicConfig(level=logging.DEBUG)
import signal
import dataset
import sys
import sqlalchemy
import json

from twitter import *
from collections import OrderedDict
from itertools import islice


class Worker(object):
    def __init__(self, name, client):
        self.name = name
        self.client = client
        self.throttled_time = False

    @property
    def throttled(self):
        print("Worker %s throttled until %s" % (self.name, self.throttled_time))
        return self.throttled_time and time() < self.throttled_time

    def throttle_until(self, epoch=None):
        self.throttled_time = int(epoch)


class WorkerQueue(object):
    def __init__(self):
        self.queue = set()
        self.index = 0

    def ready(self, worker):
        self.queue.add(worker)

    def _next(self):
        for worker in self.queue:
            if not worker.throttled:
                return worker
        raise Exception('No worker is available')

    @classmethod
    def from_credentials(self, cred_file):
        wq = WorkerQueue()

        with open(cred_file) as f:
            for line in f:
                cred = json.loads(line)
                c = Twitter(auth=OAuth(cred['token_key'],
                                       cred['token_secret'],
                                       cred['consumer_key'],
                                       cred['consumer_secret']))
                wq.ready(Worker(cred["user"], c))
        return wq


    def next(self, sync=False):
        if not sync:
            return self._next()
        while True:
            try:
                return self._next()
            except Exception:
                first_worker = min(self.queue, key=lambda x: x.throttled_time)
                diff = first_worker.throttled_time - time()
                print("All workers are busy. Waiting %s seconds" % diff)
                sleep(diff)


def signal_handler(signal, frame):
    print('You pressed Ctrl+C!')
    sys.exit(0)

def get_users(c, ulist, by_name=False, max_users=100):
    for ix in range(0, len(ulist), max_users):
        userslice = ",".join(ulist[ix:ix+max_users])
        if by_name:
            resp = c.users.lookup(screen_name=userslice)
        else:
            resp = c.users.lookup(user_id=userslice)
        for i in resp:
            uid = i['id']
            users.upsert(dict(uid=uid,
                            pending=True,
                            cursor=-1,
                            followers_count=i['followers_count'],
                            injson=json.dumps(i)),
                        keys=['uid'])


def extract(recursive=False, user=None, cred_file=None, initfile=None, dburi=None, extractor_name=None):
    signal.signal(signal.SIGINT, signal_handler)
    
    wq = WorkerQueue.from_credentials(cred_file)
    if not dburi:
        dburi = 'sqlite:///%s' % extractor_name

    db = dataset.connect(dburi)

    cursors = db.get_table('cursors')
    followers = db.get_table('followers')
    followers.create_column('isfollowed', sqlalchemy.types.Integer)
    followers.create_column('follower', sqlalchemy.types.Integer)
    followers.create_index(['isfollowed', 'follower'])

    users = db.get_table('users', primary_id='uid', primary_type='Integer')
    users.create_column('cursor', sqlalchemy.types.Integer)
    users.create_column('pending', sqlalchemy.types.Boolean)
    users.create_column('followers_count', sqlalchemy.types.Integer)
    users.create_column('injson', sqlalchemy.types.String)

    if not users.count(pending=True):
        screen_names = []
        user_ids = []
        if not user:
            print("No user. I will open %s" % initfile)
            with open(initfile, 'r') as f:
                for line in f:
                    user = line.strip().split(',')[0]
                    try:
                        int(user)
                        user_ids.append(user)
                    except ValueError:
                        screen_names.append(user)
        else:
            try:
                user_ids.append(int(user))
                print("Added id")
            except Exception as ex:
                print("Exception: {}".format(ex))
                print("Added screen_name")
                screen_names.append(user)
        get_users(screen_names, by_name=True)
        get_users(user_ids, by_name=False)


    total_users = users.count(pending=True)

    while users.count(pending=True) > 1:
        w = wq.next(sync=True)

        print("Using account: %s" % w.name)
        c = w.client
        candidate = users.find_one(pending=True, order_by='followers_count')
        if not candidate:
            break
        pending = True
        cursor = candidate.get('cursor', -1)
        uid = candidate['uid']

        print("#"*20)
        print("Getting %s" % uid)
        print("Cursor %s" % cursor)
        print("Pending: %s/%s" % (users.count(pending=True), total_users))
        try:
            resp = c.followers.ids(user_id=uid, cursor=cursor)
        except TwitterHTTPError as ex:
            if ex.e.code in (429, 502, 503, 504):
                limit = ex.e.headers.get('X-Rate-Limit-Reset', time() + 30)
                w.throttle_until(limit)
                continue
        if 'ids' in resp:
            print("New followers: %s" % len(resp['ids']))
            temp = []
            for i in resp['ids']:
                temp.append(dict(isfollowed=uid,
                                    follower=i))
            followers.insert_many(temp)
            total_followers = candidate['followers_count']
            fetched_followers = followers.count(isfollowed=uid)
            print("Fetched: %s/%s followers" % (fetched_followers,
                                                total_followers))
            cursor = resp["next_cursor"]
            if cursor > 0:
                pending = True
                print("Getting more followers for %s" % uid)
            else:
                cursor = -1
                pending = False
        else:
            print("Error with id %s %s" % (uid, resp))
            pending = False

        users.upsert(dict(uid=uid,
                        pending=pending,
                        cursor=cursor),
                    keys=['uid'])
        sys.stdout.flush()
        sleep(1)
