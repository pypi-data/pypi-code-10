from zope import schema
from zope.interface import Interface

try:
    # Plone <4.3
    from zope.app.container.constraints import contains
    from zope.app.container.constraints import containers
except ImportError:
    # Plone >=4.3
    from zope.container.constraints import contains
    from zope.container.constraints import containers

from rer.structured_content import structured_contentMessageFactory as _

class IFolderDeepening(Interface):
    """Description of the Example Type"""

    # -*- schema definition goes here -*-
