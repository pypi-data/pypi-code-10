import argparse
import json
import os
import sys


SUFFIX_SEP = '_'
SUFFIX_LEN = 2
CHUNK_SIZE = 50000  # Objects per file.


class JSplit(object):

    def __init__(self, *args, **kwargs):

        self.files = args
        self.suffix_sep = kwargs.get('suffix_sep', SUFFIX_SEP)
        self.suffix_len = kwargs.get('suffix_len', SUFFIX_LEN)
        self.chunk_size = kwargs.get('chunk_size', CHUNK_SIZE)

    def split(self):
        """Return 3-tuple list of chunk files: (filepath, filesize, items_num)."""

        chunks = []

        for src_path in self.files:
            with open(src_path) as src:
                data = json.load(src)
                for offset in range(0, len(data), self.chunk_size):
                    chunk_nr = offset // self.chunk_size + 1
                    chunk_path = self._chunk_path(src_path, chunk_nr)
                    with open(chunk_path, 'w') as dst:
                        chunk = data[offset:offset+self.chunk_size]
                        self.write(chunk, dst)
                    chunks.append((chunk_path, os.path.getsize(chunk_path), len(chunk)))

        return chunks

    def write(self, data, stream):
        """JSONize `data` and write to the `stream`."""

        last_index = len(data)-1
        stream.write('[')
        for index, item in enumerate(data):
            json.dump(item, stream)
            if index < last_index:
                stream.write(',\n')
        stream.write(']')

    def _chunk_path(self, src_path, chunk_nr):
        """Return path to the `chunk_nr` chunk::

            >>> JSplit(suffix_sep='_', suffix_len=3)._chunk_path('/path/to/file.json', 2)
            '/path/to/file_002.json'

            >>> JSplit(suffix_sep='_', suffix_len=4)._chunk_path('/path/to/file.json', 3)
            '/path/to/file_0003.json'

        """
        dirname, basename = os.path.split(src_path)
        basename, ext = os.path.splitext(basename)
        return os.path.join(dirname, '%s%s%s' % (basename, self._suffix(chunk_nr), ext))

    def _suffix(self, chunk_nr):
        """Return suffix for given chunk number::

            >>> JSplit(suffix_sep='_', suffix_len=3)._suffix(2)
            '_002'

            >>> JSplit(suffix_sep='_', suffix_len=3)._suffix(1234)
            '_1234'

        """
        return '%s%s' % (self.suffix_sep, str(chunk_nr).rjust(self.suffix_len, '0'))


def main():
    parser = argparse.ArgumentParser(description='Split a JSON file into pieces.')
    parser.add_argument('--suffix-sep', default=SUFFIX_SEP, help='')
    parser.add_argument('--suffix-len', default=SUFFIX_LEN, help='')
    parser.add_argument('--chunk-size', default=CHUNK_SIZE, help='')
    parser.add_argument('files', nargs='+')

    args = parser.parse_args()

    jsplit = JSplit(*args.files,
                    suffix_sep=args.suffix_sep,
                    suffix_len=args.suffix_len,
                    chunk_size=args.chunk_size)

    for stat in jsplit.split():
        print(list(zip(['filepath', 'filesize', 'items'], stat)))
