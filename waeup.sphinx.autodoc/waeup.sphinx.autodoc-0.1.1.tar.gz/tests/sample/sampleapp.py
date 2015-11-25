"""Sample module.
"""
import grok
from zope import schema
from zope.interface import Interface


class ISampleApp(Interface):
    """An application implementing: ISampleApp_docstring
    """
    pass


class ISampleAppItem(Interface):
    """An item implementing: ISampleAppItem_docstring
    """
    name = schema.TextLine(
        title=u'Name',
        )


def sample_func(param1, keyword1=None):
    """A sample func: sample_func_docstring
    """
    pass


class SampleApp(grok.Application, grok.Container):
    """The SampleApp is here to be documented: SampleApp_docstring
    """
    grok.implements(ISampleApp)


class SampleAppItem(grok.Model):
    """A SampleAppItem: SampleAppItem_docstring
    """
    grok.implements(ISampleAppItem)


class SampleAppCatalog(grok.Indexes):
    """A catalog of SampleApps installed: SampleAppCatalog_docstring
    """
    grok.site(ISampleApp)
    grok.name('sample app catalog')
    grok.context(ISampleAppItem)


# This is the only way (I guess) to attach a docstring to `grok.Indexes`.
# Regular docstrings are not recognized as such, as `grok.Indexes` is an
# instance of `grok.IndexesClass`, not a real class.
SampleAppCatalog.__doc__ = """
    A catalog of SampleApps installed: SampleAppCatalog_docstring
    """
