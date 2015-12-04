"""

Copyright 2015 Guoliang Li

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

"""

import logging
import app_config
import os
from pytube import YouTube
from pytube.exceptions import DoesNotExist
import json
from urllib2 import urlopen


log = logging.getLogger(__name__)

API_KEY = app_config.get_google_api_key()

URL_BASE_PLAYLIST_SEARCH = 'https://www.googleapis.com/youtube/v3/channels?part=contentDetails&forUsername=%s' \
                           '&key=' + API_KEY
URL_BASE_PLAYLIST_ITEMS = 'https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&playlistId=%s' \
                          '&maxResults=50&pageToken=%s&key=' + API_KEY
URL_BASE_VIDEO_INFO = 'https://www.youtube.com/watch?v=%s'

VIDEO_QLT_ORDER = ["3072p", "1080p", "720p", "520p", "480p", "360p", "240p", "144p"]
FMT_ORDER = ["mp4", "flv", "3gp", "webm"]


def ensure_folder(folder):
    if not os.path.exists(folder):
        os.makedirs(folder)


def get_best_video(youtube):
    for quality in VIDEO_QLT_ORDER:
        for fmt in FMT_ORDER:
            try:
                video = youtube.get(fmt, quality)
                if video is not None:
                    return video
            except DoesNotExist:
                pass


def get_json_from_url(url):
    response = urlopen(url, timeout=30)
    content = response.read().decode('utf-8')
    return json.loads(content)


def get_upload_playlist_id_by_user_id(user_id):
    url_playlist_search = URL_BASE_PLAYLIST_SEARCH % user_id
    log.info('Retrieving user uploads playlist id by: %s' % url_playlist_search)
    data = get_json_from_url(url_playlist_search)
    return data['items'][0]['contentDetails']['relatedPlaylists']['uploads']


def get_video_id_list_by_playlist_id(playlist_id):
    video_id_list = list()

    has_more_video = True
    next_page_token = ''

    while has_more_video:
        url_get_playlist_detail = URL_BASE_PLAYLIST_ITEMS % (playlist_id, next_page_token)
        log.debug('Retrieving playlist detail via: %s' % url_get_playlist_detail)
        print url_get_playlist_detail
        playlist_detail = get_json_from_url(url_get_playlist_detail)

        video_items = playlist_detail['items']
        for video_item in video_items:
            video_id_list.append(video_item['snippet']['resourceId']['videoId'])

        if 'nextPageToken' in playlist_detail:
            next_page_token = playlist_detail['nextPageToken']
            log.info('      > videos found: %s, more videos found, continue to load...' % len(video_id_list))
        else:
            log.info('No more video, ending...')
            has_more_video = False
            continue

    log.info('videos found: %s ' % len(video_id_list))
    return video_id_list


def get_best_video_by_video_id(video_id):
    pytube_video_info = YouTube(URL_BASE_VIDEO_INFO % video_id)
    best_video = get_best_video(pytube_video_info)
    log.debug('best video found for: %s - %s', video_id, best_video.filename)
    return best_video


def generate_file_name(video_id, video):
    return '%s_%s_%s.%s' % (video_id, video.filename, video.resolution, video.extension)


def download_all_videos_in_playlist(playlist_id, destination_folder, video_length_min_seconds=None):
    destination_folder = os.path.join(destination_folder, playlist_id)
    ensure_folder(destination_folder)

    total_downloaded = 0
    video_id_list = get_video_id_list_by_playlist_id(playlist_id)
    for video_id in video_id_list:
        video = get_best_video_by_video_id(video_id)

        # if video_length_min_seconds and video.length_seconds < video_length_min_seconds:
        #     log.info("Too short, skipped: %s < %s", (video.length_seconds, video_length_min_seconds))
        #     continue

        file_name = generate_file_name(video_id, video)
        destination_file_full_path = os.path.join(destination_folder, file_name)

        if os.path.isfile(destination_file_full_path):
            log.info('file existing in the destination folder: %s. will not download it again. ',
                     destination_file_full_path)
            continue

        log.info('downloading file: %s', file_name)
        try:
            video.download(destination_file_full_path)
            total_downloaded += 1
            log.info('[%s_%s]file downloaded: %s ' % (total_downloaded, len(video_id_list), destination_file_full_path))
        except Exception as e:
            log.error(e.args)

    log.info('download completed, videos downloaded: %s' % total_downloaded)
    return total_downloaded


def download_all_videos_by_user_id(user_id, destination_folder):
    print 'downloading videos by user_id :%s ' % user_id
    playlist_id = get_upload_playlist_id_by_user_id(user_id)
    destination_folder = os.path.join(destination_folder, user_id)
    ensure_folder(destination_folder)

    download_all_videos_in_playlist(playlist_id, destination_folder)

if __name__ == '__main__':
    print 'using key: %s ' % app_config.get_google_api_key()