import os
import re
import requests
import shutil
from bs4 import BeautifulSoup
from .utils import spend_time, get_size, Mission, colors


@spend_time
def get_photo(url, min_size, max_size):
    """Get photo from website."""
    # Some website need this to know you are not robot.
    user_agent = {'User-agent': 'spider'}
    # Get page html.
    res = requests.get(url, headers=user_agent)
    soup = BeautifulSoup(res.text, 'html.parser')

    # url: http://www.google.com/foobar
    # sitename: http://www.google.com
    # Dirname: www.google.com
    website = re.findall(r'(^https?://[^/]+/?)', url)[0]
    sitename = re.findall(r'^https?://([^/]+)/?', url)[0]
    pagename = soup.select('title')[0].text

    # Create directory.
    if not os.path.isdir(sitename):
        print('Create directory %s' % sitename)
        os.mkdir(sitename)
    if not os.path.isdir(os.path.join(sitename, pagename)):
        print('Create directory %s under %s.' % (pagename, sitename))
        os.mkdir(os.path.join(sitename, pagename))

    with Mission(func=download, max_thread=5) as m:
        # Find photo url.
        for img in soup.select('img'):
            photo_url = img['src']
            photoname = photo_url.split('/')[-1]
            # Prevent photos locate at website server.
            if not photo_url.startswith('http'):
                photo_url = website + photo_url
            filename = os.path.join(sitename, pagename, photoname)
            m.send(photo_url, filename, min_size, max_size)

    print('\nSize of all photo: %.3f kb.' %
          (get_size(os.path.join(sitename, pagename)) / 1000))


def download(photo, filename, min_size, max_size):
    res = requests.get(photo, stream=True)
    if max_size > int(res.headers.get('content-length', min_size - 1)) > min_size:
        print('Download %s' % photo)
        with open(filename, 'wb') as f:
            shutil.copyfileobj(res.raw, f)
    elif max_size > res.raw.tell() > min_size:
        print('Download %s' % photo)
        with open(filename, 'wb') as f:
            shutil.copyfileobj(res.raw, f)
    else:
        print('%sBypass %s%s' % (colors.FAIL, photo, colors.ENDC))



def get_all(filename, func):
    with open(filename, 'r') as f:
        with Mission(func=func, max_thread=1) as m:
            for url in f:
                m.send(url.strip(), 10000, 200000)
