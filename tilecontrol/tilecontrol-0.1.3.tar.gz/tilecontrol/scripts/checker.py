import os
import json
from tempfile import NamedTemporaryFile
import rasterio
import multiprocessing
import functools
import mercantile
import click
import pxmfile

try:
    from urllib.request import urlopen as urlopen   # Python 3
except:
    from urllib import urlopen as urlopen           # Python 2

mapbox_access_token = os.environ.get("mapbox_access_token")


class Counter(object):
    def __init__(self, initval=0):
        self.val = multiprocessing.Value('i', initval)
        self.lock = multiprocessing.Lock()

    def increment(self):
        with self.lock:
            self.val.value += 1

    def value(self):
        with self.lock:
            return self.val.value


class SingleTileCheck:
    """
    Checks a single tile
    """
    def __init__(self, mapID, tilezxy, mb_access_token=None):
        self.mapID = mapID
        self.tilezxy = tilezxy

        self.mapbox_access_token = None
        if mb_access_token:
            self.mapbox_access_token = mb_access_token
        elif mapbox_access_token:
            self.mapbox_access_token = mapbox_access_token
        else:
            raise AttributeError("no valid access token given")

    def getTile(self, zxy):
        """
        Gets a tile from Mapbox API and writes it to a temporary file
        """
        tmp = NamedTemporaryFile()
        img = urlopen("https://api.mapbox.com/v4/{mapID}/{z}/{x}/{y}.png?access_token={token}".format(
            mapID=self.mapID, z=zxy[0], x=zxy[1], y=zxy[2], token=self.mapbox_access_token))

        if img.getcode() != 200:
            tmp.close()
            return None, img.getcode()

        with open(tmp.name, "wb") as tmpFile:
            tmpFile.write(img.read())

        return tmp, None

    def checkCorners(self, img):
        """
        Returns alpha channel values for four corners of a file
        """
        x = [0, img.width - 1]
        y = [0, img.height - 1]
        corners = [[a, b] for a in x for b in y]
        data = img.read()[3]
        alphas = map(lambda x: data[x[0]][x[1]], corners)
        return alphas

    def checkTile(self):
        """
        Checks an individual tile for HTTP errors and nodata corners
        Returns [alpha count, HTTP error code]
        """
        zxy = self.tilezxy
        img, error = self.getTile(zxy)

        tileout_dict = {}
        tileout_dict['zxy'] = self.tilezxy
        tileout_dict['HTTPerror'] = None
        tileout_dict['nodata'] = None

        if error and not img:
            tileout_dict['HTTPerror'] = error
            return tileout_dict

        with rasterio.open(img.name) as src:
            alphas = self.checkCorners(src)
            img.close()
            tileout_dict['nodata'] = alphas.count(0)
            return tileout_dict


def checkTileFunc(mapid, mb_access_token, zxylist_size, zxy):
    global global_counter
    global_counter.increment()
    click.echo("checking %s- %d of %d tiles" % (zxy, global_counter.value(), zxylist_size))

    try:
        tc = SingleTileCheck(mapid, zxy, mb_access_token)
        tc_result = tc.checkTile()
    except:
        tc_result = {}
        tc_result['zxy'] = self.tilezxy
        tc_result['HTTPerror'] = None
        tc_result['nodata'] = None
        tc_result['tilecheckError'] = True

    return tc_result

global_counter = Counter(0)


def zxystring_convert(value):
    try:
        map(int, value.rstrip('\n').split('-'))
    except ValueError:
        return [0, 0, 0]


class TileChecker:
    """
    Class to check tile list
    Takes arguments (mapID, path-to-tile-file)
    Writes bad tile list to a file suffixed '.bad'

    with edge list and geojson filepath inputs, can output source images to requeue as well
    """
    def __init__(self, mapID, tilefile, outfile=None, mb_access_token=None, edgefile=None, allscenegeojson_file=None):
        self.mapID = mapID
        self.tilefile = tilefile
        self.tiles = self.parseTiles
        self.mapbox_access_token = mb_access_token
        self.outfile = outfile

        self.badtiles = []

        self.zxy_size = len(self.tiles)
        self.count = 0
        self.counter = Counter(0)

        self.edgefile = edgefile
        self.edge_tiles_list = []
        if self.edgefile:
            self.readEdgeList()

        self.allscenegeojson_file = allscenegeojson_file
        self.noedges_zxy = []

        self.output_dir = os.path.dirname(tilefile)

    def readEdgeList(self):
        """
        Reads a list of zxys that are on the edge
        """
        with open(self.edgefile, 'r') as ef:
            for line in ef:
                self.edge_tiles_list.append(line.lstrip().rstrip())

    def _zxystring_convert(self, value):
        try:
            return map(int, value.rstrip('\n').split('-'))
        except ValueError:
            return [0, 0, 0]

    @property
    def parseTiles(self):
        """
        Parses file of 'z-x-y' lines into array of [z,x,y]
        """

        return [self._zxystring_convert(line) for line in open(self.tilefile)]

    def findBadTiles(self):
        """
        Given list of tiles, return a list of bad (HTTP error or nodata count) tiles
        """
        procs = multiprocessing.cpu_count()
        pool = multiprocessing.Pool(processes=procs)
        with rasterio.drivers():
            tileCheckPartial = functools.partial(checkTileFunc, self.mapID, self.mapbox_access_token, self.zxy_size)
            badtiles = pool.map(tileCheckPartial, self.tiles)

        pool.close()
        pool.join()

        self.badtiles = badtiles

    def outputToFile(self):
        """
        Writes bad tile list to file, suffixed '.bad'
        """
        output = self.tilefile + '.bad'
        if self.outfile:
            output = self.outfile

        with open(output, 'wb') as outfile:
            for tile in self.badtiles:
                outfile.write('%s\n' % str(tile))

    def _ZXYtoFeature(self, tile):
        z = tile[0]
        x = tile[1]
        y = tile[2]

        bounds = mercantile.bounds(x, y, z)
        coords = [
            [bounds.west, bounds.south],
            [bounds.west, bounds.north],
            [bounds.east, bounds.north],
            [bounds.east, bounds.south],
            [bounds.west, bounds.south]
        ]

        feature = {}
        feature['type'] = 'Feature'
        feature['properties'] = {
            'tile': [x, y, z]
        }
        feature['geometry'] = {
            'type': 'Polygon',
            'coordinates': [coords]
        }

        return feature

    def outputZXYtoFile(self):
        """
        Writes bad tile list to file, suffixed '.badZXY'
        """
        output = self.tilefile + '.badZXY'
        if self.outfile:
            output = self.outfile + '.badZXY'

        with open(output, 'wb') as outfile:
            for tile in self.badtiles:
                zxy = tile['zxy']
                zxy_str = "%d-%d-%d" % (zxy[0], zxy[1], zxy[2])
                if zxy_str in self.edge_tiles_list:
                    continue

                outfile.write('%s\n' % zxy_str)

    def findSourceImages(self):
        """
        Match ZXY strings to their respective source images
        """
        zxy_to_srcimg_dict = {}
        source_images_to_retouch = []

        with open(self.allscenegeojson_file, 'r') as scenels:
            for line in scenels:
                pxmf = pxmfile.PxmFile.getfile(line.lstrip().rstrip())
                zxy_to_srcimg_dict[pxmf.getZXY()] = pxmf.getSourceImg()

        for tile in self.badtiles:
            zxy = tile['zxy']
            zxy_str = "%d-%d-%d" % (zxy[0], zxy[1], zxy[2])
            if (zxy_str in zxy_to_srcimg_dict) and (zxy_to_srcimg_dict[zxy_str] not in source_images_to_retouch):
                source_images_to_retouch.append(zxy_to_srcimg_dict[zxy_str])

        output_sourceimgs = os.path.join(self.output_dir, "%s_missing_and_nodata_sourceimgs" % (self.mapID))
        with open(output_sourceimgs, 'w') as output:
            for srcimg in source_images_to_retouch:
                output.write(srcimg + "\n")

    def outputGeojson(self, outputfile_path=None):
        """
        Outputs failing files to geojson
        """
        output = {}
        output['type'] = 'FeatureCollection'
        output['features'] = []

        if outputfile_path is None:
            outputfile_path = self.tilefile + "_missingNodata.geojson"

        for tile_dict in self.badtiles:
            if tile_dict['HTTPerror'] or tile_dict['nodata']:
                feature = self._ZXYtoFeature(tile_dict['zxy'])
                output['features'].append(feature)

        writeout = json.dumps(output, separators=(',', ':'))
        with open(outputfile_path, 'w') as f_out:
            f_out.write(writeout)

        return outputfile_path
