import imp
import logging

import os
import argparse

from rabbit_youtube import youtube_utils


def main():
    print 'main...'
    parser = argparse.ArgumentParser(description='Passing parameter for rabbit youtube....')

    parser.add_argument('--youtube_user_id', '-u', help='youtube user id')
    parser.add_argument('--playlist_id', '-p', help='youtube playlist id')
    parser.add_argument('download_to', help='video files download to...')

    args = parser.parse_args()

    user_id = args.youtube_user_id
    play_list_id = args.playlist_id
    download_to = args.download_to

    if user_id:
        print 'going to download all videos uploaded by user_id: %s to: %s' % (user_id, download_to)
        youtube_utils.download_all_videos_by_user_id(user_id, download_to)
    elif play_list_id:
        print 'going to download all videos from playlist_id:%s to :%s' % (play_list_id, download_to)
        youtube_utils.download_all_videos_in_playlist(play_list_id, download_to)
    else:
        print 'Please specify youtube_user_id or playlist_id'


if __name__ == '__main__':
    log_format = "%(asctime)s [%(name)s] [%(levelname)-5.5s]  %(message)s"
    logging.basicConfig(level=logging.DEBUG,
                        format=log_format,
                        datefmt="%H:%M:%S", filemode='a')
    consoleHandler = logging.StreamHandler()
    consoleHandler.setLevel(logging.INFO)
    consoleHandler.setFormatter(logging.Formatter(log_format))
    logging.getLogger(__name__).addHandler(consoleHandler)

    main()
