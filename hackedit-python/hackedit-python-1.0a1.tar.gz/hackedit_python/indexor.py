import locale
from hackedit import api
from pyqode.core.cache import Cache
from pyqode.core.share import Definition
from pyqode.python.backend import defined_names


class PySymbolIndexor(api.plugins.SymbolIndexorPlugin):
    mimetypes = ['text/x-python']

    def parse(self, path):
        if path.endswith('_rc.py'):
            return []
        try:
            encoding = Cache().get_file_encoding(path)
        except KeyError:
            encoding = locale.getpreferredencoding()
        try:
            with open(path, encoding=encoding) as f:
                code = f.read()
        except UnicodeDecodeError:
            try:
                with open(path, encoding='utf-8') as f:
                    code = f.read()
            except UnicodeDecodeError:
                # could not deduce encoding
                return []
        request_data = {
            'path': path,
            'code': code
        }
        results = defined_names(request_data)
        return [Definition.from_dict(ddict) for ddict in results]
