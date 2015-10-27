from zope.i18nmessageid import MessageFactory

# Define permission string, so we can import it if needed.  See also
# the permission in configure.zcml.
UseSearchAndReplace = "collective.searchandreplace: Use Search And Replace"
# Message factory:
SearchAndReplaceMessageFactory = MessageFactory('SearchAndReplace')


def initialize(context):
    """Initializer called when used as a Zope 2 product."""
