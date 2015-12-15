import DateTime
from Products.CMFCore.utils import getToolByName

def modification_made(obj, event):
    # get portal object and set the last_modified_header
    portal = getToolByName(obj, 'portal_url').getPortalObject()
    portal.last_modified_header = DateTime.now()