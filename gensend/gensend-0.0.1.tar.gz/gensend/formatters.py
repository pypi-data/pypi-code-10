from os import linesep
from json import JSONEncoder
from csv import DictWriter as CsvDictWriter


def formatter_factory(fp, format):
    formatter = CsvFormatter(fp)

    if 'txt' in format:
        formatter = TextFormatter(fp)
    elif 'json' in format:
        formatter = JsonFormatter(fp)
    return formatter


class Formatter():
    def __init__(self, fp):
        self.fp = fp

    def iterout(self, iterable):
        if iterable is None:
            return
        try:
            header = next(iterable)

            if hasattr(header, 'keys'):
                self.begin(header.keys())
            else:
                self.begin(header)
            self.out(header)
            for item in iterable:
                self.out(item)
            self.end()
        except StopIteration:
            pass

    def out(self, d):
        raise NotImplementedError('Formatters must provide a row method.')

    def begin(self, fields):
        return self.out(fields)

    def end(self):
        pass


class TextFormatter(Formatter):
    def begin(self, fields):
        pass

    def out(self, d):
        self.fp.write(str(d) + linesep)


class JsonFormatter(Formatter):
    def begin(self, fields):
        self.encoder = JSONEncoder(indent=2, separators=(', ', ': '))

    def iterout(self, iterable):
        self.begin([])
        for chunk in self.encoder.iterencode(list(iterable)):
            self.fp.write(chunk)

    def out(self, d):
        self.fp.write(self.encoder.encode(d))


class CsvFormatter(Formatter):
    def begin(self, fields):
        self.writer = CsvDictWriter(self.fp, fieldnames=fields)
        self.writer.writeheader()

    def out(self, d):
        self.writer.writerow(d)
