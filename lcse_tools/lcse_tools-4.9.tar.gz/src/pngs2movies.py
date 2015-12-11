#!/usr/bin/env python

import argparse
import os
import re
import subprocess
import tempfile

from PIL import Image, ImageDraw, ImageFont

import lcse
from lcse_tools import image_util as iu

def filter_files(path, prefix=None, suffix=None):
  # Switch to https://docs.python.org/2/library/fnmatch.html

  cond = lambda x : (x.startswith(prefix) if prefix else True) and (x.endswith(suffix) if suffix else True)
  return [os.path.join(path, f) for f in os.listdir(path) if cond(f)]

# 1. Create temp directory to work in
# 2. Fully composite image
# 3. Write out to temp file (don't overwrite if it exists)
# 4. Make movie

def add_time_to_pngs(image_path, prefix, font_name, temp_prefix, time_map={}, font_size=50):

  print temp_prefix
  print font_name

  temp_path = os.path.join(temp_prefix, prefix)

  if not os.path.exists(temp_path):
    os.makedirs(temp_path)

  font = ImageFont.truetype(font_name, font_size)

  image_files = filter_files(image_path, suffix='.png')
  image_files.sort()

  dump_re = re.compile('(.*)([-_])([\d]{4,6})(.*)')

  prefix = os.path.basename(os.path.commonprefix(image_files))

  for filename in image_files:

    m = dump_re.match(filename)

    if not m:
      continue

    dump = int(m.group(3))
    filename_out = os.path.join(temp_path, os.path.basename(filename))

    if os.path.exists(filename_out):
      continue

    im = Image.open(filename)
    iu.draw_time(im, font, dump=dump, time=time_map.get(dump))

    print filename, '->', filename_out

    im.save(filename_out)

  return temp_path

def make_movie_from_pngs(image_path, **kwargs):
  prefix = kwargs.get('prefix', '')

  add_time = kwargs.get('add_time')

  if add_time is not None:
    if add_time:
      rtp = lcse.rtplot_reader(add_time)
      time_map = dict((dump, val['T']) for dump, val in rtp.dump_map.items())
    else:
      time_map = {}

    image_path = add_time_to_pngs(image_path, prefix, kwargs.get('font'), kwargs.get('tmp_dir'), time_map,
                                  font_size=kwargs.get("font_size"))

  video_prefix = kwargs.get('video_prefix', prefix)
  fps = kwargs.get('fps', 24)
  tune = kwargs.get('tune', 'stillimage')
  threads = str(kwargs.get('threads', 'auto'))

  print prefix

  files = filter_files(image_path, prefix=prefix, suffix='.png')
  dumps = [int(f[-8:-4]) for f in files]
  dumps.sort()

  if not dumps:
    print "Nothing found for %s in %s" % (prefix, image_path)
    return

  dmin, dmax = min(dumps), max(dumps)

  video_suffix = kwargs.get('video_suffix') + "_%s" % str(fps) if kwargs.get('video_suffix') else "_%s" % str(fps)
  video_filename = '%s_%04i-%04i_%s.avi' % (video_prefix, dmin, dmax, video_suffix)
  video_path = os.path.abspath(os.path.join(kwargs.get('movies_path', '.'), video_filename))

  if not os.path.exists(kwargs.get('movies_path', '.')):
    os.makedirs(kwargs.get('movies_path', '.'))

  print "vide_path", video_path, os.path.exists(video_path)

  if os.path.exists(video_path):
    print "File %s exists, skipping" % video_path
    return

#  return

    # Make Video
  args = ['mencoder', 'mf://%s*.png' % prefix,
          '-mf', 'fps=%i:type=png' % fps,
          '-oac', 'copy',
          '-ovc', 'x264', '-x264encopts',
          'preset=veryslow:tune=%s:crf=15:frameref=15:fast_pskip=0:threads=%s' % (tune, threads),
          '-o', video_path]

  print ' '.join(args)
  print image_path
  print("Output file is %s" % video_path)

  p = subprocess.Popen(args, cwd=image_path)
  s, i = p.communicate()
  p.wait()

def main():

  parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)

  parser.add_argument('-i', help='Path to images base directory',  default='.')
  parser.add_argument('-o', help='Path to video save directory', default='.')
  parser.add_argument('--fps', nargs='+',type=int, help='List of fps to create', default=[18])
  parser.add_argument('--prefixes', nargs='+', help='List of prefixes to try. Otherwise everything inside input-path is used')
  parser.add_argument('--video-prefix', help='Prefix to add to each video in this', default='')
  parser.add_argument('--video-suffix', help='Suffix to add to each video in this', default='')

  parser.add_argument('--add-time', nargs='*', help='Specify RTplot.ppm file to use for timing info')
  parser.add_argument('--font', help='Font to use', default='/home/stou/workspace/lcse_tools/fonts/Roboto-Bold.ttf')
  parser.add_argument('--font-size', type=int, help='Size of font to use', default=50)
  parser.add_argument('--tmp-dir', help='Temporary directory to store intermediate files', default='/tmp/timed')

  args = parser.parse_args()

  if args.prefixes:
    prefixes = args.prefixes
  else:
    prefixes = os.listdir(args.i)
    prefixes.sort()

  print "Using prefixes", prefixes, args.i, args.o

  for fps in args.fps:
    for prefix in prefixes:
      try:
        print 'Making %s at %s' % (prefix, os.path.join(args.i, prefix))
        make_movie_from_pngs(os.path.join(args.i, prefix), prefix=prefix,
                             video_prefix=args.video_prefix + prefix,
			     video_suffix=args.video_suffix,
                             fps=fps, movies_path=args.o, font=args.font,
                             add_time=args.add_time, tmp_dir=args.tmp_dir,
                             font_size=args.font_size)
      except Exception as e:
        print "Problem", e

  return

if __name__ == '__main__':
  main()
