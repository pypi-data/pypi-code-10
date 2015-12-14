from Products.Archetypes.public import TextField
from Products.Archetypes.public import RichWidget
from archetypes.schemaextender.field import ExtensionField
from zope.component import adapts
from zope.interface import implements
from archetypes.schemaextender.interfaces import ISchemaExtender
from archetypes.schemaextender.interfaces import IBrowserLayerAwareExtender
from Products.Archetypes.public import TextField
from Products.CMFBibliographyAT.interface import IBibliographicItem
from humboldt.cmfbibliographyat.interfaces import IBibLayer
from humboldt.cmfbibliographyat import _

class BibliographicItemText(ExtensionField, TextField):
    """TextField containing a tabel of contents"""

class BibliographicItemExtender(object):
    adapts(IBibliographicItem)
    implements(ISchemaExtender, IBrowserLayerAwareExtender)

    layer = IBibLayer
    
    fields = [
        BibliographicItemText(
                name="table_of_contents",
                searchable=1,
                required=0,
                default_content_type='text/html',
                default_output_type='text/x-html-safe',
                allowable_content_types=('text/structured',
                                         'text/restructured',
                                         'text/html',
                                         'text/plain',),
                widget=RichWidget(
                    label=_(u"Table of contents"),
           ),
        ),
    ]

    def __init__(self, context):
        self.context = context

    def getFields(self):
        return self.fields
