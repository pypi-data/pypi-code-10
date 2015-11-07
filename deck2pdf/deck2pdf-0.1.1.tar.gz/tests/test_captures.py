import os
from pytest import raises
from deck2pdf import errors
from . import (
    current_dir,
    test_dir,
)


class TestForCaptureEngine(object):
    @property
    def _class(self):
        from deck2pdf.captures import CaptureEngine
        return CaptureEngine

    def test_init_not_resource(self):
        raises(errors.ResourceNotFound, self._class, ('test'))

    def test_init_exists_resource(self):
        engine = self._class('tests/testslide/index.rst')
        assert engine.url == 'file://{}/{}'.format(test_dir, 'testslide/index.rst')
        assert engine.save_dir == os.path.join(current_dir, '.deck2pdf')

    def test_init_web_resource(self):
        engine = self._class('http://example.com/')
        assert engine.url == 'http://example.com/'
        assert engine.save_dir == os.path.join(current_dir, '.deck2pdf')

    def test_start_for_save_dir(self):
        engine = self._class('http://example.com/')
        import shutil
        import glob
        shutil.rmtree(engine.save_dir, True)
        engine.start()
        assert os.path.exists(engine.save_dir) is True
        files = glob.glob('{}/*'.format(engine.save_dir))
        assert len(files) == 0

    def test_capture_page_is_abstract(self):
        engine = self._class('http://example.com/')
        raises(NotImplementedError, engine.capture_page, ())

    def test_capture_all_is_abstract(self):
        engine = self._class('http://example.com/')
        raises(NotImplementedError, engine.capture_all)


class CommonTestForCaptureEngine(object):
    @property
    def _class(self):
        from deck2pdf.captures import stub
        return stub.CaptureEngine

    def test_init(self):
        # Same to TestForCaptureEngine.test_init_web_resource
        engine = self._class('http://example.com/')
        assert engine.url == 'http://example.com/'
        assert engine.save_dir == os.path.join(current_dir, '.deck2pdf')


class TestForPhantomJsCaptureEngine(CommonTestForCaptureEngine):
    @property
    def _class(self):
        from deck2pdf.captures import phantomjs
        return phantomjs.CaptureEngine


class TestForGhostpyCaptureEngine(CommonTestForCaptureEngine):
    @property
    def _class(self):
        from deck2pdf.captures import ghostpy
        return ghostpy.CaptureEngine


class TestForFindEngine(object):
    def test_not_found(self):
        from deck2pdf.captures import find_engine
        assert find_engine('noengine') is None

    def test_found_ghostpy(self):
        from deck2pdf.captures import find_engine
        from deck2pdf.captures.ghostpy import CaptureEngine
        engine = find_engine('ghostpy')
        assert engine == CaptureEngine


def test_resolve_path():
    from deck2pdf.captures import resolve_path
    assert resolve_path('http://example.com') == 'http://example.com'
    assert resolve_path('https://example.com') == 'https://example.com'
    assert resolve_path('tests/testslide/index.rst') == 'file://{}/{}'.format(test_dir, 'testslide/index.rst')
    raises(errors.ResourceNotFound, resolve_path, ('not_found'))
