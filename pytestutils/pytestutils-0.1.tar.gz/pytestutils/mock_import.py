import __builtin__
import mock
import pytest

orig_import = __builtin__.__import__

def _get_fromlist(args):
    #https://docs.python.org/2/library/functions.html#__import__
    if len(args) == 4 and isinstance(args[-1], int):
        return args[-2]
    elif len(args) == 3 and isinstance(args[-1], tuple):
        return args[-1]
    else:
        return ()

def _check_fromlist(targets, fromlist):
    for target in targets:
        for inner in fromlist:
            if target in inner:
                return True                
    return False

def _check_namelist(targets, name):
    for target in targets:
        if target in name:
            return True
    return False


@pytest.fixture
def return_mock_imports(request, monkeypatch):
    imp_mods_to_mock = request.cls.__dict__.get('import_modules_to_mock', [])
    imp_names_to_mock = request.cls.__dict__.get('import_names_to_mock', [])
    monkeypatch.setattr(__builtin__, '__import__', mock_imports(imp_mods_to_mock, request.cls.import_names_to_mock))

def mock_imports(name_targets, from_targets=[]):
    def mock_out_import(name, *args, **kwargs):
        if args and from_targets:
            fromlist = _get_fromlist(args)
            if _check_fromlist(from_targets, fromlist):
                return mock.MagicMock()
        if _check_namelist(name_targets, name):
            return mock.MagicMock()
        return orig_import(name, *args, **kwargs)
    return mock_out_import
