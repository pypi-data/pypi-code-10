from json_compare.json_compare import are_same, contains, json_are_same

__version__ = '0.2.11'
VERSION = tuple(map(int, __version__.split('.')))

__all__ = ['are_same', 'contains', 'json_are_same']
