from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer
import argparse
import os
import sys
import time
import yaml

verbose=False
debug=False
config_filename = 'roadwarrior.yaml'


class PushEventHandler(FileSystemEventHandler):
  def __init__(self, local, remote):
    self.local_base = local
    self.remote_base = remote

  def on_any_event(self, event):
    if event.is_directory:
      return
    local = event.src_path
    assert(local.startswith(self.local_base))
    relative_path = local[len(self.local_base):]
    remote = os.path.join(self.remote_base, relative_path)
    rsync_push(local, remote)


def parse_config(local_root):
  config_file = os.path.join(local_root, config_filename)
  config = yaml.load(open(config_file, "r"))
  remote_root = config['remote']
  for local, remote in config['mapping'].items():
    yield (os.path.join(local_root, local, ''),
           os.path.join(remote_root, remote, ''))


def rsync(*args):
  args = list(args)
  if debug:
    args = ['-v'] + args
  if verbose:
    args = ['--out-format=\'%n\''] + args

  cmd = 'rsync ' + ' '.join(args)
  if debug:
    print("$", cmd)
  os.system(cmd)


def rsync_push(local, remote):
  if verbose:
    print(local, ' -> ', remote)
  else:
    print("Push", local)
  rsync('-rlpt --update -z', local, remote)


def rsync_checkout(remote, local):
  if verbose:
    print(remote, ' -> ', local)
  else:
    print("Checkout", remote)
  if not os.path.exists(local):
    os.makedirs(local)
  rsync('-rlpt -z --delete', remote, local)


def push(path):
  for local, remote in parse_config(path):
    rsync_push(local, remote)


def watch(path):
  observer = Observer()

  for local, remote in parse_config(path):
    observer.schedule(PushEventHandler(local, remote), local, recursive=True)
  observer.start()
  print("Watching...")
  try:
    while True:
      time.sleep(1)
  except KeyboardInterrupt:
      observer.stop()
  observer.join()


def checkout(path):
  for local, remote in parse_config(path):
    rsync_checkout(remote, local)


def main():
  parser = argparse.ArgumentParser(description='')
  parser.add_argument('--checkout', '-c', action='store_true')
  parser.add_argument('--verbose', '-v', action='store_true')
  parser.add_argument('--debug', '-d', action='store_true')
  parser.add_argument('--watch', '-w', action='store_true')
  parser.add_argument('--push', '-p', action='store_true')

  parser.add_argument('paths', nargs='*')

  args = parser.parse_args()

  global verbose
  global debug
  verbose = args.verbose
  debug = args.debug

  if not args.paths:
    args.paths = ['.']

  for path in args.paths:
    if args.checkout:
      checkout(path)
    if args.watch:
      watch(path)
    if args.push:
      push(path)

if __name__ == '__main__':
  main()
