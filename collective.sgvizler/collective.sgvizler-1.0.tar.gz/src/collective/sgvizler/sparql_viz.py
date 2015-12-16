
from z3c.form import group, field
from zope import schema
from zope.interface import invariant, Invalid
from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm

from plone.dexterity.content import Item
from plone.autoform import directives as form

from plone.app.textfield import RichText
from plone.namedfile.field import NamedImage, NamedFile
from plone.namedfile.field import NamedBlobImage, NamedBlobFile
from plone.namedfile.interfaces import IImageScaleTraversable

from plone.supermodel import model
from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from collective.sgvizler import _

from vocabularies import charts
from vocabularies import output_mode


# Interface class; used to define content-type schema.

class ISPARQLViz(model.Schema, IImageScaleTraversable):
    """
    SPARQL Visualization
    """

    # Fiedlsets


    model.fieldset('query',
            label=u"Query",
            fields=[ 'endpoint', 'vizmode', 'style', 'squery',]
        )

    model.fieldset('advanced',
        label=u"Advanced",
        fields=['endpoint_output', 'externalrdf']
    )

    # Fields

    figure_title = schema.TextLine(
        title=_(u'sgvizler_sparqlviz_figure_title_title',
            default=u'Figure Title'),
        required=False,
    )

    form.widget('squery', rows=20)
    squery = schema.SourceText(
        title=_(u'sgvizler_sparqlviz_query_title',
            default=u'Query'),
        #cols=12,
        required=True,
    )

    endpoint = schema.TextLine(
        title=_(u'sgvizler_sparqlviz_endpoint_title',
            default=u'SPARQL Endpoint'),
        required=True,
    )

    vizmode = schema.Choice(
        title=_(u'sgvizler_sparqlviz_vizmode_title',
            default=u'Vizualisation Mode'),
        vocabulary=charts,
        default=u'sgvizler.visualization.Table',
        required=True,
    )

    style = schema.TextLine(
        title=_(u'sgvizler_sparqlviz_style_title',
            default=u'Inline Style'),
        required=False,
    )

    externalrdf = schema.Text(
        title=_(u'sgvizler_sparqlviz_externalrdf_title',
            default=u'A string of URLs to RDF files'),
        description=_(u'sgvizler_sparqlviz_externalrdf_description',
                      default=u"""List of URLs to RDF files. The list must be separated by |-characters, and the configured SPARQL endpoint must allow FROMs in the query.&#13;
Note that data-sgvizler-rdf is just a shorthand way of telling Sgvizler to include a list of FROMs in the query. The configured endpoint reads the listed RDF files and executes the query on them; this means that the files must be accessible to the endpoint and the endpoint must be setup to allow FROM in queries."""),
        required=False,
    )

    endpoint_output = schema.Choice(
        title=_(u'sgvizler_sparqlviz_endpoint_output_title',
            default=u'Endpoint Output'),
        vocabulary=output_mode,
        default=u'json',
        required=True,
    )

class SPARQLViz(Item):

    # Add your class methods and properties here
    pass


# View class
# The view is configured in configure.zcml. Edit there to change
# its public name. Unless changed, the view will be available
# TTW at content/@@sampleview

class SampleView(BrowserView):
    """ sample view class """

    index = ViewPageTemplateFile('sparql_viz_templates/sampleview.pt')

#    def __init__(context, request):
#        self.context = context
#        self.request = request

    def __call__(self):
        return self.render()

    def render(self):
        return self.index()
