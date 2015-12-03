import pykka
import logging
import thread
import threading
from datetime import datetime, timedelta
from email.utils import parsedate_tz
from mopidy import core
from twython import TwythonStreamer
from mopidy.audio import PlaybackState


def to_datetime(datestring):
    time_tuple = parsedate_tz(datestring.strip())
    dt = datetime(*time_tuple[:6])
    return dt - timedelta(seconds=time_tuple[-1])


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

        thread.start_new_thread(self.twitterstream.user, ())

def on_stop(self):
        self.log.info('TwitterDJ Streamer is stopping')
        self.twitterstream.stop()


class InputQueue(pykka.ThreadingActor):
    def __init__(self, core, username, playlist):
        super(InputQueue, self).__init__()
        self.username = username
        self.core = core
        self.playlistUri = playlist
        self.log = logging.getLogger('mopidy_twitterdj_queue')

    def on_start(self):
        self.log.info('TwitterDJ Queue is starting')

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
                self.log.info('TwitterDJ is feeling lucky and will queue %s - %s', result.tracks[0].artists, result.tracks[0].name)
                self.add_to_playlist(result.tracks[0])
                self.log.info('Tracks in list: '+str(len(self.core.tracklist.get_tl_tracks().get())))
                self.play()
            else:
                self.log.warning('TwitterDJ could not find a track for '+artist+' - '+track)
                return

    def queue(self, track):
        self.core.tracklist.add([track])

    def add_to_playlist(self, track):
        playlist = self.get_playlist()
        appended_tracks = list(playlist.tracks)
        if track not in appended_tracks:
            appended_tracks.append(track)
            playlist = playlist.copy(tracks=appended_tracks)
            self.core.playlists.save(playlist)
            self.queue(track)
        else:
            self.log.info('Track %s - %s already in playlist', track.artists, track.name)

    def play(self):
        state = self.core.playback.get_state().get()
        if state == PlaybackState.STOPPED:
            self.core.playback.play()
        elif state == PlaybackState.PAUSED:
            self.core.playback.resume()
        elif state == PlaybackState.PLAYING:
            return

    def get_playlist(self):
        """
        :rtype: :class:`mopidy.models.Playlist` or :class:`None`
        """
        return self.core.playlists.lookup(self.playlistUri).get()

    def update_playlist(self):
        self.log.info('TwitterDJ: updating playlists')
        self.core.playlists.refresh()


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
        self.master = config['twitterdj']['master']
        self.queue_ref = None
        self.twitter_source = None
        self.playlistPosition = 0

    def on_start(self):
        self.log.info('Starting TwitterDJ')
        if self.master:
            self.update_time()
            self.log.info("Master mode: Will write to shared spotify playlist")
            if not self.playlistUri:
                self.log.error("Playlist URI not set. Please add playlist=uri to config")
            self.queue_ref = InputQueue.start(core=self.core, username=self.username, playlist=self.playlistUri)
            self.twitter_source = TwitterSource.start(config=self.config, queue_ref=self.queue_ref)
        else:
            self.log.info("TwitterDJ running in slave mode: Playing shared playlist")
            self.log.warning("Slave mode: Will not write to shared spotify playlist")
            self.play_playlist()

    def on_stop(self):
        self.log.info('Stopping TwitterDJ')
        if self.twitter_source:
            self.twitter_source.stop()
        if self.queue_ref:
            self.queue_ref.stop()

    def update_time(self):
        self.last_event = datetime.now()
        self.log.info('TwitterDJ accepting mentions from after '+str(self.last_event))

    def play(self):
        self.core.playback.play()

    def play_playlist(self):
        self.core.tracklist.clear()
        playlist = self.core.playlists.lookup(self.playlistUri).get()
        if not playlist:
            self.log.error("Unable to lookup spotify playlist %s"+self.playlistUri)
        self.core.tracklist.add(playlist.tracks)
        self.play()

        if len(playlist.tracks) == 0:
            self.log.info('** Playlist empty. Waiting 5s')
            threading.Timer(5.0, self.play_playlist).start()
        else:
            self.log.info('Tracks in list: %s', len(self.core.tracklist.get_tl_tracks().get()))

    def check_while_waiting(self):
        playlist = self.core.playlists.lookup(self.playlistUri).get()
        tracklist = self.core.tracklist.get_tl_tracks().get()
        if len(tracklist) > 0:
            last_track = tracklist[-1].track
        else:
            last_track = None
        self.core.tracklist.clear()
        self.core.tracklist.add(tracks=playlist.tracks)
        tracklist = self.core.tracklist.get_tl_tracks().get()
        if last_track:
            if playlist.tracks.index(last_track) < len(playlist.tracks) -1: # new tracks available
                last_tracks = self.core.tracklist.filter(uri=[last_track.uri]).get()
                if len(last_tracks) > 0:
                    self.core.playback.play(tl_track=tracklist[tracklist.index(last_tracks[0])+1])
            else:
                threading.Timer(5.0, self.check_while_waiting).start()
                self.log.info('** Waiting to resume playback')
        else:
            if len(tracklist) == 0:
                threading.Timer(5.0, self.check_while_waiting).start()
                self.log.info('** Nothing to play')
            else:
                self.play()
                self.log.info('** Finally something to play')

    def refresh_playlist(self):
        playlist = self.core.playlists.lookup(self.playlistUri).get()
        tracklist = self.core.tracklist.get_tl_tracks().get()
        current_idx = self.core.tracklist.index().get()
        try:
            current_pl_idx = playlist.tracks.index(tracklist[current_idx].track)
        except ValueError:
            current_pl_idx = None

        if current_pl_idx: # selected track available
            non_current_tracks = tracklist
            del non_current_tracks[current_idx]
            tlids_to_remove = map(lambda tltrack : tltrack.tlid, non_current_tracks)
            self.core.tracklist.remove({'tlid':tlids_to_remove})
            self.core.tracklist.add(tracks=playlist.tracks[:current_pl_idx],at_position=0)
            self.core.tracklist.add(tracks=playlist.tracks[current_pl_idx+1:])

    def track_playback_started(self, tl_track):
        self.refresh_playlist()
        self.log.info('** PLAY %s - %s ', tl_track.track.artists, tl_track.track.name)

    def track_playback_ended(self, tl_track, time_position):
        self.log.info('** END %s - %s ', tl_track.track.artists, tl_track.track.name)
        if self.core.tracklist.index(tl_track).get() == (self.core.tracklist.get_length().get() - 1):
            threading.Timer(5.0, self.check_while_waiting).start()
            self.log.info('** Waiting for new tracks')
