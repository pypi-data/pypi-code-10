# tests for waeup.sphinxext.autodoc
import grok
import os
import py.path
import pytest
import shutil
from six import StringIO
# Import TestApp under different name: TestNAMEs are treated special
# by py.test.
from sphinx_testing import TestApp as SphinxTestApp
from waeup.sphinx.autodoc import is_indexes_object, autodoc_skip_member


LOCAL_TEST_DIR = py.path.local(os.path.dirname(__file__) or '.')
SAMPLE_SPHINX_SRC = LOCAL_TEST_DIR / "sample"


@pytest.fixture(scope="function")
def doc_src_dir(request, tmpdir):
    """A fixture that provides a sample source dir as found in regular `docs`.

    Contains the files from local sample dir (including conf.py, etc.) but
    is set in a temporary dir, so we can remove it any time or change the
    file therein.
    """
    source = tmpdir / "source"
    shutil.copytree(str(SAMPLE_SPHINX_SRC), str(source))
    return source


@pytest.fixture(scope="session")
def static_sphinx(request):
    """A fixture that provides a static sphinx build.

    'static' means: the HTML docs are built once and results can be
    retrieved during test session.

    After test session all generated stuff (files etc.) is removed.
    """
    exc = None
    status = StringIO()
    warning = StringIO()
    app = SphinxTestApp(
        buildername='html', srcdir=SAMPLE_SPHINX_SRC,
        copy_srcdir_to_tmpdir=True, status=status, warning=warning,
        verbosity=2)
    try:
        app.build()
    except Exception as _exc:
        exc = _exc
    if app:
        if exc:
            request.addfinalizer(app.cleanup, error=exc)
        else:
            request.addfinalizer(app.cleanup)
    app.status = status
    app.warning = warning
    return app


class SampleCatalogClass(grok.Indexes):
    pass


class TestAutodoc(object):

    def test_is_indexes_object(self):
        # we can tell whether something is an instance of grok.Indexes
        assert is_indexes_object(object()) is False
        assert is_indexes_object(SampleCatalogClass) is True

    def test_autodoc_skip_member(self):
        # by default we return the passed in status
        assert autodoc_skip_member(
            None, 'module', 'MyObject', object(), True, {}) is True
        assert autodoc_skip_member(
            None, 'module', 'MyObject', object(), False, {}) is False

    def test_autodoc_skip_member_allows_grok_indexes(self):
        # we do not skip grok.Indexes
        assert autodoc_skip_member(
            None, 'mod', 'MyName', SampleCatalogClass, True, {}) is False
        assert autodoc_skip_member(
            None, 'mod', 'MyName', SampleCatalogClass, False, {}) is False

    def test_build_succeeded(self, static_sphinx):
        # we get a message that build succeeded
        status = static_sphinx.status.getvalue()
        assert "build succeeded" in status

    def test_regular_class_is_documented(self, static_sphinx):
        # regular classes are documented
        html = (static_sphinx.outdir / 'contents.html').read_text()
        assert 'SampleApp_docstring' in html

    def test_indexes_are_documented(self, static_sphinx):
        # grok.Indexes are documents
        html = (static_sphinx.outdir / 'contents.html').read_text()
        assert 'SampleAppCatalog' in html

    def test_indexes_docstrings_are_shown(self, static_sphinx):
        # grok.Indexes' docstrings are processed.
        html = (static_sphinx.outdir / 'contents.html').read_text()
        assert 'SampleAppCatalog_docstring' in html

    def test_indexes_get_processed(self, static_sphinx):
        # status output documents that catalogs are processed
        assert "[autodoc] getattr(_, u'SampleAppCatalog')" in (
            static_sphinx.status.getvalue())


class TestDottedNamedMembers(object):
    # tests for componentes helping to ignore members with dots in name

    def test_have_config_var(self, static_sphinx):
        # The config has a config var for ignoring member names with dots
        assert hasattr(static_sphinx.config, 'ignore_dot_named_members')
        assert static_sphinx.config.ignore_dot_named_members is True  # default

    def test_set_config_var(self, doc_src_dir):
        # we can set the config var in `conf.py` (to false)
        doc_src_dir.join("conf.py").write(
            "\nignore_dot_named_members = False\n", mode="a")
        app = SphinxTestApp(buildername='html', srcdir=str(doc_src_dir))
        assert hasattr(app.config, 'ignore_dot_named_members')
        assert app.config.ignore_dot_named_members is False

    def test_set_config_var_true(self, doc_src_dir):
        # we can set the config var in `conf.py` to true
        doc_src_dir.join("conf.py").write(
            "\nignore_dot_named_members = True\n", mode="a")
        app = SphinxTestApp(buildername='html', srcdir=str(doc_src_dir))
        assert hasattr(app.config, 'ignore_dot_named_members')
        assert app.config.ignore_dot_named_members is True

    def test_ignore_dot_named_members_avoids_errors(self, doc_src_dir):
        # setting `ignore_dot_named_members` really helps
        doc_src_dir.join("conf.py").write(
            "\nignore_dot_named_members = True\n", mode="a")
        status = StringIO()
        warning = StringIO()
        app = SphinxTestApp(
            buildername='html', srcdir=str(doc_src_dir),
            status=status, warning=warning, verbosity=0)
        app.build()
        assert "AttributeError" not in warning.getvalue()

    def test_ignore_dot_named_helps_only_if_enabled(self, doc_src_dir):
        # setting `ignore_dot_named_members` does not help if disabled.
        doc_src_dir.join("conf.py").write(
            "\nignore_dot_named_members = False\n", mode="a")
        status = StringIO()
        warning = StringIO()
        app = SphinxTestApp(
            buildername='html', srcdir=str(doc_src_dir),
            status=status, warning=warning, verbosity=0)
        app.build()
        assert "AttributeError" in warning.getvalue()


class TestGrokIndexesDirective(object):

    def test_sig_prefix(self, static_sphinx):
        # grokindexes directive gets ``class`` as prefix
        html = (static_sphinx.outdir / 'contents.html').read_text()
        assert "SomeCatalog" in html

    def test_autogrokindexes_works(self, static_sphinx):
        # the autogrokindexes directive is processed
        html = (static_sphinx.outdir / 'contents.html').read_text()
        snippet = html.split('Explicitly requested auto content')[1]
        snippet = snippet.split('Manually added content')[0]
        assert 'SampleAppCatalog' in snippet
