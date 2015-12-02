import requests
import base64
from datetime import datetime, timedelta

class Dabs(object):
    url = 'http://www.skyguide.ch/fileadmin/dabs-%(day)s/DABS_%(date)s.pdf'

    def _url(self, tomorrow=False):
        return self.url % {
            "day": 'today' if not tomorrow else 'tomorrow',
            "date": datetime.now().strftime('%Y%m%d') if not tomorrow else (datetime.now() + timedelta(days=1)).strftime('%Y%m%d')
        }

    def _download(self, url):
        r = requests.get(url, stream=True)
        if r.status_code == requests.codes.ok:
            r.raw.decode_content = True
            return base64.b64encode(r.raw.read())

    @property
    def today(self):
        return self._download(self._url())

    @property
    def tomorrow(self):
        return self._download(self._url(tomorrow=True))


if __name__ == "__main__":
    dabs = Dabs()

    with open('today.pdf', 'w') as f:
        f.write(base64.b64decode(dabs.today))

    with open('tomorrow.pdf', 'w') as f:
        f.write(base64.b64decode(dabs.tomorrow))