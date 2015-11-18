import logging

from zerotest.record.formatter import Formatter


LOG = logging.getLogger(__name__)


class Generator(object):
    """
    Generator test scripts from record data
    """

    def __init__(self, filepath, options=None, match_options=None):
        self._filepath = filepath
        default_options = dict(verify_ssl=False)
        if options:
            default_options.update(options)

        self._options = options or dict()
        self._formatter = Formatter()
        self._match_options = match_options or dict()

    def generate(self):
        """
        return None if records data not found
        :return:
        """

        import codecs

        records = []
        with codecs.open(self._filepath, 'r', 'utf-8') as record_file:
            while True:
                result = self._formatter.read_record(record_file)
                if not result:
                    break
                records.append(result)

        from zerotest.generator.python.render import Renderer

        if len(records) == 0:
            return None

        renderer = Renderer(options=self._options,
                            match_options=self._match_options)

        return renderer.render(records)
