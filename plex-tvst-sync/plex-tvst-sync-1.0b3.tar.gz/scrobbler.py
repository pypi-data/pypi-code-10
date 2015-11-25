import errno
import os
import shelve
import time
import sys

import appdirs
from plexapi.server import PlexServer
import requests

TVST_CLIENT_ID = 'DksvfcwLfe6tk7-K-bAf'
TVST_CLIENT_SECRET = 'BLAtFZJqah5lqrQZSlLLDHGpff5rJw2xa_iDyR9N'

_dirs = appdirs.AppDirs('plex-tvst-sync')

try:
    os.makedirs(_dirs.user_cache_dir)
except OSError, e:
    if e.errno != errno.EEXIST:
        raise

_db = shelve.open(os.path.join(_dirs.user_cache_dir, 'db'))
_plex_server = PlexServer()


def tvst_request(method, endpoint, **kwargs):
    time.sleep(6)  # lazy man's rate-limiting
    
    if not endpoint.startswith('oauth/'):
        kwargs.setdefault('params', {})
        kwargs['params']['access_token'] = _db['tvst_access_token']
    
    url = 'https://api.tvshowtime.com/v1/' + endpoint    
    r = requests.request(method, url, **kwargs)
    
    return r.json()


def run_tvst_oauth_flow():
    def request_device_info():
        data = {'client_id': TVST_CLIENT_ID}
        r = tvst_request('POST', 'oauth/device/code', data=data)
        return r
    
    def request_access_token():
        data = {
            'client_id': TVST_CLIENT_ID,
            'client_secret': TVST_CLIENT_SECRET,
            'code': device_info['device_code'],
        }
        r = tvst_request('POST', 'oauth/access_token', data=data)
        return r
    
    device_info = request_device_info()
    print 'Code:', device_info['device_code']
    print device_info['verification_url']
    
    while True:
        access_token_info = request_access_token()
        
        if access_token_info['result'] == 'OK':
            _db['tvst_access_token'] = access_token_info['access_token']
            break
        else:
            time.sleep(device_info['interval'])


def get_tvst_library():
    shows = []
    current_page = 0
    limit = 100
    
    while True:
        params = {'page': current_page, 'limit': limit}
        r = tvst_request('GET', 'library', params=params)
        page_shows = r['shows']
        
        for show in page_shows:
            if not show['archived']:
                shows.append(show)
        
        if len(page_shows) < limit:
            break
        
        current_page += 1
    
    return shows


def get_tvst_show(show_id):
    params = {'show_id': show_id, 'include_episodes': '1'}
    r = tvst_request('GET', 'show', params=params)
    return r['show']


def search_plex_show(name):
    matching_shows = _plex_server.library.search(name, vtype='show')
    
    for show in matching_shows:
        if show.title == name:
            return show
    
    return None


def checkin_plex_episode(episode):
    episode.markWatched()


def checkin_tvst_episode(episode_id):
    data = {'episode_id': episode_id}
    tvst_request('POST', 'checkin', data=data)


def main():
    if not _db.get('tvst_access_token'):
        run_tvst_oauth_flow()
        sys.exit(0)
    
    for tvst_show in get_tvst_library():
        show_name = tvst_show['name']
        plex_show = search_plex_show(show_name)
        
        if not plex_show:  # Plex doesn't have that show
            continue
        
        print show_name
        
        tvst_episodes = get_tvst_show(tvst_show['id'])['episodes']
        plex_episodes = plex_show.episodes()
        
        for tvst_episode in tvst_episodes:
            tvst_season_no = int(tvst_episode['season_number'])
            tvst_episode_no = int(tvst_episode['number'])
            
            print 'S%02dE%02d' % (tvst_season_no, tvst_episode_no)
            
            for plex_episode in plex_episodes:
                plex_season_no = int(plex_episode.season().index)
                plex_episode_no = int(plex_episode.index)
                
                tvst_watched = tvst_episode['seen']
                plex_watched = (plex_episode.viewCount > 0)
                
                if (plex_season_no == tvst_season_no and
                        plex_episode_no == tvst_episode_no):  # same episode
                    if tvst_watched and not plex_watched:
                        checkin_plex_episode(plex_episode)
                        print 'Checked in on Plex'
                    elif plex_watched and not tvst_watched:
                        checkin_tvst_episode(tvst_episode['id'])
                        print 'Checked in on TVST'
        
        print


if __name__ == '__main__':
    main()
