import os
import sys
import httplib2
import base64
import math
import copy
import string
import datetime

from geojson import Polygon, Feature, FeatureCollection, GeometryCollection
from urlparse import urlparse
import json

from .base import resolutions
from .tilemath import getMaxX, getMaxY

def getNearbyTiles(ix0, iy0, iz0, ir, size=256, bbox=[-20037508.34,-20037508.34,20037508.34,20037508.34]):
    nearbyTiles = []

    if iz0 == 0:
        return nearbyTiles

    res = resolutions[int(iz0)]
    maxX = getMaxX(res, size, bbox)
    maxY = getMaxY(res, size, bbox)

    for iy1 in range(iy0-ir,iy0+ir+1):
        for ix1 in range(ix0-ir,ix0+ir+1):
            if iy1 != iy0 or ix1 != ix0:
                iy1 = iy1 % maxY
                ix1 = ix1 % maxX
                t = (ix1, iy1, iz0)
                nearbyTiles.append(t)

    return nearbyTiles

def getParentTiles(ix0, iy0, iz0, depth=-1, size=256, bbox=[-20037508.34,-20037508.34,20037508.34,20037508.34]):
    parentTiles = []

    res = resolutions[int(iz0)]
    maxX = getMaxX(res, size, bbox)
    maxY = getMaxY(res, size, bbox)

    levels = range(iz0-depth, iz0) if depth != -1 else range(0, iz0)
    for iz1 in levels:
        ix1 = int(ix0 / math.pow(2, iz0-iz1))
        iy1 = int(iy0 / math.pow(2, iz0-iz1))
        t = (ix1, iy1, iz1)
        parentTiles.append(t)

    return parentTiles


def getChildrenTiles(ix0, iy0, iz0, depth, minZoom, maxZoom, size=256, bbox=[-20037508.34,-20037508.34,20037508.34,20037508.34]):
    childrenTiles = []

    res = resolutions[int(iz0)]
    maxX = getMaxX(res, size, bbox)
    maxY = getMaxY(res, size, bbox)

    iz1 = max(iz0, minZoom)
    t = (ix0, iy0, iz1)
    d1 = depth-(iz1-iz0)
    childrenTiles = nav_down([], t, d1, maxZoom)
    return childrenTiles

def nav_down(tiles, t, d, max):
    x, y, z = t
    if z == max or d <= 0:
        tiles.append(t)
        return tiles
    else:
        t00 = x * 2, y * 2, z + 1
        t01 = x * 2, y * 2 + 1, z +1
        t10 = x * 2 + 1, y * 2, z + 1
        t11 =  x * 2 + 1, y * 2 + 1, z + 1
        tiles = nav_down(tiles, t00, d-1, max)
        tiles = nav_down(tiles, t01, d-1, max)
        tiles = nav_down(tiles, t10, d-1, max)
        tiles = nav_down(tiles, t11, d-1, max)
        return tiles

