import base64
import posixpath
from StringIO import StringIO
from os.path import splitext

import PIL.Image
from Products.CMFCore.utils import getToolByName
from collective.jsonmigrator import logger
from collective.transmogrifier.interfaces import ISection, ISectionBlueprint
from collective.transmogrifier.transmogrifier import Transmogrifier
from plone.app.blob.interfaces import IATBlob
from zope.component.hooks import getSite
from zope.interface import classProvides, implements

from resilient_blueprints import wrap_and_reregister_blueprints


TYPE_SUBSTITUTION = {
    'Large Plone Folder': 'Folder',
    'ATAudio': 'File',
    'ATVideo': 'File',
}


class MigraPMCustomBlueprint(object):

    classProvides(ISectionBlueprint)
    implements(ISection)

    def __init__(self, transmogrifier, name, options, previous):
        self.previous = previous
        self.remote_path = str(options['remote-path'].strip('/'))
        self.destiny_path = str(options['destiny-path'].strip('/'))

    def __iter__(self):
        for item in self.previous:
            path = item['_path']

            # Remove strange layout from old ATAudio/ATVideo types (and other bad or usued fields)
            #  Note that these types will be substituted by "File" afterwards (see TYPE_SUBSTITUTION use)
            if item['_type'] in ['ATAudio', 'ATVideo']:
                remove_fields(item, [
                    '_layout',
                    'album', 'artist', 'audioTitle', 'cacheStatus', 'comment', 'year'])

            # CONVERT 'image/x-ms-bmp' TO PNG
            if '_datafield_image' in item and item['_datafield_image']['content_type'] == 'image/x-ms-bmp':
                convert_bmp_to_png(item)

            # PORTAL_WINDOWZ (ASSUMES WINDOWZ IS INSTALLED HERE)
            if 'portal_windowZ' in path:
                portal_windowz = getSite().portal_windowz
                portal_windowz.setBase_url(unicode(item['base_url']))
                portal_windowz.setPage_width(unicode(item['page_width']))
                portal_windowz.setPage_height(unicode(item['page_height']))
                portal_windowz.setHttp_proxy(unicode(item['http_proxy']))
                portal_windowz.setDynamic_window(item['dynamic_window'])
                continue

            # SKIP
            if posixpath.basename(path.strip('/')) in {'syndication_information',
                                                       'crit__created_ATSortCriterion',
                                                       'crit__Type_ATPortalTypeCriterion',
                                                       'lista-eventos',
                                                       'lista-noticias',
                                                       }:
                logger.info(':: ACTUALLY SKIPPED -> ' + path)
                continue

            # REWRITE PATH
            assert path.startswith(self.remote_path)
            item['_path'] = self.destiny_path + path[len(self.remote_path):]

            # ADJUST TYPES
            original_type = item['_type']
            if original_type in TYPE_SUBSTITUTION:
                item['_type'] = TYPE_SUBSTITUTION[original_type]
                logger.warn(':: TYPE TYPE_SUBSTITUTED (%s -> %s) in %s' % (original_type, item['_type'], path))

            # CHANGE ALL WORKFLOWS TO 'simple_publication_workflow'
            if '_workflow_history' in item:
                values = item['_workflow_history'].values()
                if values:
                    # There should be exactly one key, value pair, if any. We change the key
                    assert len(values) == 1
                    item['_workflow_history'] = {'simple_publication_workflow': values[0]}

            # RENAME CONTENT WITH id == 'index_html' TO JUST 'index'
            container, id = posixpath.split(item['_path'].strip('/'))
            if id == 'index_html':
                item['_path'] = '/'.join((container, 'index'))

            # AVOID HAVING 'index_html' SET AS THE DEFAULT PAGE OF AN IMAGE
            #   ATBlob.index_html is a method in Image)
            # Without this we would hit a bug here:
            # plone.app.transmogrifier-1.3-py2.7.egg/plone/app/transmogrifier/browserdefault.py:50
            if item['_type'] in ['Image', 'File'] and item.get('_defaultpage', None) == 'index_html':
                del item['_defaultpage']

            # FLOWPLAYER LAYOUT
            if item['_type'] == 'File' \
                and '_datafield_file' in item \
                and item['_datafield_file']['content_type'] in [
                    'audio/mpeg',
                    'audio/x-mp3',
                    'audio/x-mpeg',
                    'audio/mp3',
                    'video/mp4',
                    'video/x-flv',
                    'application/x-flash-video',
                    'flv-application/octet-stream',
                    'video/flv',
            ]:
                item['_layout'] = 'flowplayer'

            yield item


def remove_fields(item, fields):
    for field in fields:
        if field in item:
            del item[field]


def convert_bmp_to_png(item):
    image_data = item['_datafield_image']
    filename, data, content_type, encoding = [image_data[k] for k in ['filename', 'data', 'content_type', 'encoding']]
    original_decoded = base64.b64decode(data)
    input = StringIO(original_decoded)
    image = PIL.Image.open(input)
    output = StringIO()
    image.save(output, 'PNG')
    png_decoded = output.getvalue()
    png_data = base64.b64encode(png_decoded)

    basename, ext = splitext(filename)
    if ext.lower() == '.bmp':
        png_filename = basename + '.png'
    else:
        png_filename = filename

    item['_datafield_image'] = {
        'size': len(png_decoded),
        'filename': png_filename,
        'data': png_data,
        'content_type': 'image/png',
        'encoding': 'base64'
    }
    logger.info("@@@@ Image Converted from [%s] to [%s] in [%s]" % (filename, png_filename, item['_path']))


class MigraPMFixBlobContentTypeBlueprint(object):

    '''It seems that Blob File method .setContentType is bugged,
        so we forcefully set the content type.
    '''

    classProvides(ISectionBlueprint)
    implements(ISection)

    def __init__(self, transmogrifier, name, options, previous):
        self.previous = previous
        self.context = transmogrifier.context

    def __iter__(self):
        for item in self.previous:
            if '_datafield_file' in item and 'content_type' in item['_datafield_file']:
                obj = self.context.unrestrictedTraverse(item['_path'].lstrip('/'), None)
                if IATBlob.providedBy(obj):
                    self.setBlobContentType_hack(obj, item['_datafield_file']['content_type'])
            yield item

    def setBlobContentType_hack(self, blob_file, value):
        '''Hack to directcly set content type of a blob file.

        Based on

        Products.Archetypes-1.9.7-py2.7.egg/Products/Archetypes/BaseObject.py
            BaseObject.setContentType

        plone.app.blob-1.5.9-py2.7.egg/plone/app/blob/field.py
            BlobField.getContentType (note that there is no setContentType in this class)
        '''
        field = blob_file.getPrimaryField()
        if field:
            blob = field.getUnwrapped(blob_file)
            blob.setContentType(value)


BLUEPRINT_IDS_TO_WRAP = [
    'collective.jsonmigrator.remotesource',
    'collective.transmogrifier.sections.manipulator',
    'collective.transmogrifier.sections.constructor',
    'plone.app.transmogrifier.atschemaupdater',
    'plone.app.transmogrifier.uidupdater',
    'plone.app.transmogrifier.browserdefault',
    'collective.jsonmigrator.datafields',
    'collective.jsonmigrator.workflowhistory',
    'collective.jsonmigrator.properties',
    'collective.jsonmigrator.owner',
    'collective.jsonmigrator.local_roles',
    'collective.jsonmigrator.mimetype',
    'collective.jsonmigrator.skipitems',
    'pm2_custom',
    'pm2_fix_blob_content_type',
]


def run_migration(context, overrides, session):

    # Migrate

    logger.info(">>>>>>>> Start of importing")

    tracebacks = wrap_and_reregister_blueprints(BLUEPRINT_IDS_TO_WRAP, session)
    Transmogrifier(context)('interlegis.portalmodelo.migrator', **overrides)

    logger.info(">>>>>>>> End of importing")

    # Adjust things afterwards

    try:
        wf_tool = getToolByName(context, 'portal_workflow')
        wf_tool.updateRoleMappings()
    except Exception, e:
        logger.error('An error occurred while updating the workflow mappings:\n' + e.message)
    else:
        logger.info(">>>>>>>> Worflow mappings updated")
    try:
        catalog = getToolByName(context, 'portal_catalog')
        catalog.clearFindAndRebuild()
    except Exception, e:
        logger.error('An error occurred while updating the catalog:\n' + e.message)
    else:
        logger.info(">>>>>>>> Catalog updated")

    return tracebacks
