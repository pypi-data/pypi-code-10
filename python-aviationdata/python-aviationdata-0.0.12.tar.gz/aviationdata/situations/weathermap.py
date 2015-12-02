import requests
import base64

class Weathermap(object):
    baseUrl = 'http://www.dwd.de/bvbw/generator/DWDWWW/Content/Oeffentlichkeit/KU/KUPK/Hobbymet/Wetterkarten/Analysekarten/'

    groundPressureMapUrl = 'Analysekarten__Default__Boden__Europa__Luftdruck__Bild,property=default.png'
    pressureMap850hpaUrl = 'Analysekarten__Default__Hoehe__850hPa-HT__Europa__Bild,property=default.png'

    def _download(self, url):
        r = requests.get(url, stream=True)
        if r.status_code == requests.codes.ok:
            r.raw.decode_content = True
            return base64.b64encode(r.raw.read())

    @property
    def groundPressureMap(self):
        return self._download("%s%s" % (self.baseUrl, self.groundPressureMapUrl))

    @property
    def airPressureMap(self):
        return self._download("%s%s" % (self.baseUrl, self.pressureMap850hpaUrl))

if __name__ == "__main__":
    weathermap = Weathermap()

    with open('groundPressureMap.png', 'w') as f:
        f.write(base64.b64decode(weathermap.groundPressureMap))

    with open('airPressureMap.png', 'w') as f:
        f.write(base64.b64decode(weathermap.airPressureMap))