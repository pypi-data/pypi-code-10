from .Tile import TileShape
from .Map import Map

from PIL import Image, ImageDraw

import math

def _draw_shape(draw, shape, x, y, mat):
  coords = []
  if shape == TileShape.FULL:
    coords.append((x, y))
    coords.append((x + 1, y))
    coords.append((x + 1, y + 1))
    coords.append((x, y + 1))
  elif shape == TileShape.BIG_1:
    coords.append((x, y))
    coords.append((x + 1, y + 0.5))
    coords.append((x + 1, y + 1))
    coords.append((x, y + 1))
  elif shape == TileShape.SMALL_1:
    coords.append((x, y + 0.5))
    coords.append((x + 1, y + 1))
    coords.append((x, y + 1))
  elif shape == TileShape.BIG_5:
    coords.append((x + 1, y))
    coords.append((x, y + 0.5))
    coords.append((x, y + 1))
    coords.append((x + 1, y + 1))
  elif shape == TileShape.SMALL_5:
    coords.append((x + 1, y + 0.5))
    coords.append((x, y + 1))
    coords.append((x + 1, y + 1))
  elif shape == TileShape.HALF_A:
    coords.append((x, y))
    coords.append((x + 1, y + 1))
    coords.append((x, y + 1))

  if coords:
    for (i, (x, y)) in enumerate(coords):
      coords[i] = (mat[0][0] * x + mat[0][1] * y + mat[0][2],
                   mat[1][0] * x + mat[1][1] * y + mat[1][2])
    draw.polygon(coords, 'white')
    return
    
  if shape <= TileShape.SMALL_4:
    shape = 1 + ((shape - TileShape.BIG_1) - 2) % 8
  elif shape <= TileShape.SMALL_8:
    shape = 9 + ((shape - TileShape.BIG_5) + 2) % 8
  else:
    shape = 17 + ((shape - TileShape.HALF_A) - 1) % 4

  nmat = [[mat[0][1], -mat[0][0], 0],
          [mat[1][1], -mat[1][0], 0],
          [0, 0, 1]]
  nmat[0][2] = mat[0][0] * x + mat[0][1] * y + mat[0][2] - (
                        nmat[0][0] * (x + 0)  + nmat[0][1] * (y + 1))
  nmat[1][2] = mat[1][0] * x + mat[1][1] * y + mat[1][2] - (
                        nmat[1][0] * (x + 0)  + nmat[1][1] * (y + 1))
  _draw_shape(draw, shape, x, y, nmat)

def tilt_map(map, mat, acc = 3):
  tile_layer = {}
  for ((layer, x, y), tile) in map.tiles.items():
    if not layer in tile_layer:
      tile_layer[layer] = {}
    tile_layer[layer][(x, y)] = tile

  for i in range(3):
    for j in range(3):
      mat[i][j] *= acc

  masks = {}
  xmn = xmx = ymn = ymx = False
  for dx in range(2):
    for dy in range(2):
      tx = (x + dx) * mat[0][0] + (y + dy) * mat[0][1] + mat[0][2]
      ty = (x + dx) * mat[1][0] + (y + dy) * mat[1][1] + mat[1][2]
      if xmn == False:
        xmn = xmx = tx
        ymn = ymx = ty
      else:
        xmn = min(xmn, tx)
        xmx = max(xmx, tx)
        ymn = min(ymn, ty)
        ymx = max(ymx, ty)

  xmn = int(math.floor(xmn))
  xmx = int(math.ceil(xmx))
  ymn = int(math.floor(ymn))
  ymx = int(math.ceil(ymx))

  draw_mat = mat
  draw_mat[0][2] -= xmn
  draw_mat[1][2] -= ymn
  width = xmx - xmn + 1
  height = ymx - ymn + 1

  for shape in TileShape:
    img = Image.new("1", (width, height))
    draw = ImageDraw.Draw(img)
    _draw_shape(draw, shape, x, y, draw_mat)

  map = Map()
  for (layer, tiles) in tile_layer.items():
    xmn = xmx = ymn = ymx = False
    for (x, y) in tiles.keys():
      for dx in range(2):
        for dy in range(2):
          tx = (x + dx) * mat[0][0] + (y + dy) * mat[0][1] + mat[0][2]
          ty = (x + dx) * mat[1][0] + (y + dy) * mat[1][1] + mat[1][2]
          if xmn == False:
            xmn = xmx = tx
            ymn = ymx = ty
          else:
            xmn = min(xmn, tx)
            xmx = max(xmx, tx)
            ymn = min(ymn, ty)
            ymx = max(ymx, ty)

    xmn = int(math.floor(xmn))
    xmx = int(math.ceil(xmx))
    ymn = int(math.floor(ymn))
    ymx = int(math.ceil(ymx))
    draw_mat = mat
    draw_mat[0][2] -= xmn
    draw_mat[1][2] -= ymn
    width = xmx - xmn + 1
    height = ymx - ymn + 1

    img = Image.new("1", (width, height))
    draw = ImageDraw.Draw(img)
    for ((x, y), tile) in tiles.items():
      _draw_shape(draw, tile.shape, x, y, draw_mat)

    for (ind, px) in enumerate(img.getdata()):
      x = ind % width
      y = ind // width
      #print(x, y, px)
    if layer == 19:
      img.show("Layer %d" % layer)
