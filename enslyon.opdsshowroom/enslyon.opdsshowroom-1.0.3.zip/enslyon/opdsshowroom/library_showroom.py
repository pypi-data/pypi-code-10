
from z3c.form import group, field
from zope import schema
from zope.interface import invariant, Invalid
from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm

from plone.dexterity.content import Item

from plone.app.textfield import RichText
from plone.namedfile.field import NamedImage, NamedFile
from plone.namedfile.field import NamedBlobImage, NamedBlobFile
from plone.namedfile.interfaces import IImageScaleTraversable

from plone.supermodel import model
from Products.Five import BrowserView

from requests import request
from lxml import html

from enslyon.opdsshowroom import MessageFactory as _


# Interface class; used to define content-type schema.

class ILibraryShowroom(model.Schema, IImageScaleTraversable):
    """
    Create a Showroom for an OPDS Library from an eXistDB
    """

    # If you want a schema-defined interface, delete the model.load
    # line below and delete the matching file in the models sub-directory.
    # If you want a model-based interface, edit
    # models/library_showroom.xml to define the content type.

    model.load("models/library_showroom.xml")


# Custom content-type class; objects created for this content type will
# be instances of this class. Use this class to add content-type specific
# methods and properties. Put methods that are mainly useful for rendering
# in separate view classes.

class LibraryShowroom(Item):

    # Add your class methods and properties here
    pass


# View class
# The view is configured in configure.zcml. Edit there to change
# its public name. Unless changed, the view will be available
# TTW at content/@@showroom_view

class ShowroomView(BrowserView):
    """ Showroom view class """

    # Add view methods here
    def renderXQuery(self):
        """ Render the HTML > body result """ 

        context = self.context
        headers = {'charset': 'UTF-8'}
        xquery_response = request('GET', context.xquery_request_url, headers=headers)
        html_text = html.document_fromstring(xquery_response.text)
        return html.tostring(html_text.xpath('/html/body')[0])

