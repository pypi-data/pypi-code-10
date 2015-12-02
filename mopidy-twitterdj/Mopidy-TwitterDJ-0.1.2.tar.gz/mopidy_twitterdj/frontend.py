import pykka
import logging
import copy_reg
import types

from datetime import datetime, timedelta
from email.utils import parsedate_tz
from mopidy import core
from twython import Twython, TwythonStreamer
from multiprocessing import Pool
from collections import deque


def to_datetime(datestring):
    time_tuple = parsedate_tz(datestring.strip())
    dt = datetime(*time_tuple[:6])
    return dt - timedelta(seconds=time_tuple[-1])

def _pickle_method(m):
    if m.im_self is None:
        return getattr, (m.im_class, m.im_func.func_name)
    else:
        return getattr, (m.im_self, m.im_func.func_name)

copy_reg.pickle(types.MethodType, _pickle_method)


class UserStreamer(TwythonStreamer):
    def __init__(self, username, queue_ref, *args, **kwargs):
        self.queue_ref = queue_ref
        self.username = username
        self.log = logging.getLogger('mopidy_twitterdj_streamer')
        self.stopping = False
        super(UserStreamer, self).__init__(*args, **kwargs)

    def on_success(self, data):
        if self.stopping:
            self.disconnect()
        if 'text' in data:
            self.on_tweet(data)

    def on_error(self, status_code, data):
        if self.stopping:
            self.disconnect()
        self.log.warning(str(status_code) + ' - ' + data)
        self.keepalive()

    def on_tweet(self, data):
        sent = False
        if 'entities' in data:
            if 'user_mentions' in data['entities']:
                for user in data['entities']['user_mentions']:
                    if 'screen_name' in user and user['screen_name'].lower() == self.username:
                        message = {'msg': 'add', 'data': {'requester': data['user']['screen_name'], 'text':data['text'], 'created_at':data['created_at']}}
                        self.log.info('Streamer sent tweet: '+str(message))
                        self.queue_ref.tell(message)
                        sent = True
        if not sent:
            self.keepalive()

    def keepalive(self):
        message = {'msg': 'stillalive'}
        try:
            self.queue_ref.tell(message)
        except:
            self.disconnect()

    def stop(self):
        self.stopping = True
        self.disconnect()


class TwitterSource(pykka.ThreadingActor):
    def __init__(self, config, queue_ref):
        super(TwitterSource, self).__init__()
        self.config = config
        self.queue_ref = queue_ref
        self.log = logging.getLogger('mopidy_twitterdj_source')
        self.consumerkey = config['twitterdj']['consumerkey']
        self.consumersecret = config['twitterdj']['consumersecret']
        self.token = config['twitterdj']['token']
        self.secret = config['twitterdj']['secret']
        self.username = config['twitterdj']['username']
        self.username = self.username.lower()
        self.twitterstream = None

    def on_start(self):
        self.log.info('TwitterDJ Streamer is starting')
        self.twitterstream = UserStreamer(self.username, self.queue_ref, self.consumerkey, self.consumersecret, self.token, self.secret)
        self.log.info('Listening to mentions of @'+ self.username)
        pool = Pool(processes=1)              # Start a worker processes.
        pool.apply_async(self.twitterstream.user, [], None)

def on_stop(self):
        self.log.info('TwitterDJ Streamer is stopping')
        self.twitterstream.stop()


class InputQueue(pykka.ThreadingActor):
    def __init__(self, core, username, playlist):
        super(InputQueue, self).__init__()
        self.username = username
        self.core = core
        self.playlist = None
        self.playlistUri = playlist
        self.log = logging.getLogger('mopidy_twitterdj_queue')

    def on_start(self):
        self.log.info('TwitterDJ Queue is starting')
        #self.update_playlist()

    def on_stop(self):
        self.log.info('TwitterDJ Queue is stopping')

    def on_receive(self, message):
        if 'msg' in message:
            if message['msg'] == 'add':
                if 'data' in message:
                    self.process_tweet(message['data'])
            elif message['msg'] == 'stillalive':
                return

    def process_tweet(self, tweet):
        text = tweet['text'].lower()
        text = text.replace('@'+self.username, '')
        text = text.strip()
        self.process_text(text)

    def process_text(self, text):
        elements = text.split('-', 1)
        if len(elements) < 2:
            self.log.warning('Could not parse tweet')
            return
        self.search(elements[0].lower().strip(),elements[1].lower().strip())

    def search(self, artist, track):
        results = self.core.library.search({'artist': [artist],'track_name':[track]}, uris=['spotify:']).get()
        for result in results:
            if result.tracks and len(result.tracks) > 0:
                self.log.info('TwitterDJ is feeling lucky and will queue ' + result.tracks[0].name)
                self.queue(result.tracks[0])
                self.log.info('Tracks in list: '+str(len(self.core.tracklist.get_tl_tracks().get())))
                self.play()
            else:
                self.log.warning('TwitterDJ could not find a track for '+artist+' - '+track)
                return

    def queue(self, track):
        self.core.tracklist.add([track])

    def play(self):
        state = self.core.playback.get_state().get()
        if state == 'STOPPED':
            self.core.playback.play()
        elif state == 'PAUSED':
            self.core.playback.resume()
        elif state == 'PLAYING':
            return

    def update_playlist(self):
        self.log.info('TwitterDJ: updating playlist')
        self.core.playlists.refresh()
        self.playlist = self.core.playlists.lookup(self.playlistUri).get()


class TwitterDJFrontend(pykka.ThreadingActor, core.CoreListener):
    def __init__(self, config, core):
        super(TwitterDJFrontend, self).__init__()
        self.core = core
        self.config = config
        self.last_event = None
        self.log = logging.getLogger('mopidy_twitterdj_frontend')
        self.username = config['twitterdj']['username']
        self.username = self.username.lower()
        self.playlist = None
        self.playlistUri = config['twitterdj']['playlist']
        self.queue_ref = None
        self.twitter_source = None

    def on_start(self):
        self.log.info('Starting TwitterDJ')
        self.update_time()
        self.queue_ref = InputQueue.start(core=self.core, username=self.username, playlist=self.playlistUri)
        self.twitter_source = TwitterSource.start(config=self.config, queue_ref=self.queue_ref)

    def on_stop(self):
        self.log.info('Stopping TwitterDJ')
        self.twitter_source.stop()
        self.queue_ref.stop()


    def update_time(self):
        self.last_event = datetime.now()
        self.log.info('TwitterDJ accepting mentions from after '+str(self.last_event))

    def play(self):
        self.core.playback.play()

    def find_next(self):
        try:
            next = self.queue.popleft()
        except IndexError:
            self.log.info('TwitterDJ has nothing to find')
