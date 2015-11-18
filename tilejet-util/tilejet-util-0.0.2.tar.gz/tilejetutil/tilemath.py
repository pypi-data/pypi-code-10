import math
from geojson import Polygon, Feature, FeatureCollection, GeometryCollection

from .base import resolutions, webmercator_bbox, D2R, R2D 

#===============#
# Bounding Box Functions
# Standard bounding box order is:
# - minX, minY, maxX, maxY or
# - West, South, East, North

def bbox_to_wkt(x0, y0, x1, y1, srid="4326"):
    if None not in [x0, y0, x1, y1]:
        wkt = 'SRID=%s;POLYGON((%s %s,%s %s,%s %s,%s %s,%s %s))' % (
            srid, x0, y0, x0, y1, x1, y1, x1, y0, x0, y0)
    else:
        return None


def llbbox_to_mercator(llbbox):
    minlonlat = forward_mercator([llbbox[0], llbbox[1]])
    maxlonlat = forward_mercator([llbbox[2], llbbox[3]])
    return [minlonlat[0], minlonlat[1], maxlonlat[0], maxlonlat[1]]


def mercator_to_llbbox(bbox):
    minlonlat = inverse_mercator([bbox[0], bbox[1]])
    maxlonlat = inverse_mercator([bbox[2], bbox[3]])
    return [minlonlat[0], minlonlat[1], maxlonlat[0], maxlonlat[1]]


def forward_mercator(lonlat):
    x = lonlat[0] * 20037508.34 / 180
    try:
        n = math.tan((90 + lonlat[1]) * math.pi / 360)
    except ValueError:
        n = 0
    if n <= 0:
        y = float("-inf")
    else:
        y = math.log(n) / math.pi * 20037508.34
    return (x, y)


def bbox_intersects(a,b):
    return ( a[0] < b[2] and a[2] > b[0] ) and ( a[1] < b[3] and a[3] > b[1] )


def getMaxX(res, size, bbox):
    maxX = int(
        round(
            (bbox[2] - bbox[0]) /
            (res * size)
        )
    ) - 1
    return maxX

def getMaxY(res, size, bbox):
    maxY = int(
        round(
            (bbox[3] - bbox[1]) /
            (res * size)
        )
    ) - 1
    return maxY

# Flip Y Coordinate.
# Equation to flip y is the same in both directions
def flip_y(x, y, z, size=256, bbox=[-20037508.34,-20037508.34,20037508.34,20037508.34]):
    res = resolutions[int(z)]
    maxY = int(
        round(
            (bbox[3] - bbox[1]) /
            (res * size)
        )
    ) - 1
    return maxY - y


def tms_to_bbox(x,y,z):
    e = tile_to_lon(x+1,z)
    w = tile_to_lon(x,z)
    s = tile_to_lat(y+1,z)
    n = tile_to_lat(y,z)
    return [w, s, e, n]


def tms_to_geojson(x,y,z):
    bbox = tms_to_bbox(x,y,z)
    minx = bbox[0]
    miny = bbox[1]
    maxx = bbox[2]
    maxy = bbox[3]
    geom = Polygon([[(minx,miny),(maxx,miny),(maxx,maxy),(minx,maxy),(minx,miny)]])
    return geom


def tile_to_lon(x, z):
    return (x/math.pow(2,z)*360-180);


def tile_to_lat(y, z):
    n = math.pi - 2 * math.pi * y / math.pow(2,z);
    return ( R2D * math.atan(0.5*(math.exp(n)-math.exp(-n))));


def tms_to_quadkey(x,y,z):
    quadKey = []
    for i in range(z,0,-1):
        digit = 0
        mask = 1 << ( i - 1)
        if ((x & mask) != 0):
            digit += 1
        if ((y & mask) != 0):
            digit += 1
            digit += 1
        quadKey.append(str(digit));

    return ''.join(quadKey);


# quadkey_to_tms:
# u strong be a string representation
def quadkey_to_tms(u):
    iz = len(u)
    ix = quadkey_to_x(u)
    iy = quadkey_to_y(u)
    return iz, ix, iy


def quadkey_to_x(u):
    x = 0
    for i in range(0,len(u)):
        x = x * 2
        if ( int(u[i]) == 1 ) or ( int(u[i]) == 3 ):
            x += 1
    return x


def quadkey_to_y(u):
    y = 0
    for i in range(0,len(u)):
        y = y * 2
        if ( int(u[i]) == 2 ) or ( int(u[i]) == 3 ):
            y += 1
    return y
