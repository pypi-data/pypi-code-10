# -*- coding: utf-8 -*-
from AccessControl import ClassSecurityInfo
from Acquisition import aq_base
from Acquisition import aq_inner
from Acquisition import aq_parent
from ComputedAttribute import ComputedAttribute
from OFS.ObjectManager import REPLACEABLE
from OFS.interfaces import IOrderedContainer as IOrderedContainer
from Products.Archetypes.atapi import BaseFolder
from Products.CMFCore.permissions import View
from plone.folder.ordered import OrderedBTreeFolderBase
from webdav.NullResource import NullResource
from zope.interface import implementer
from App.class_init import InitializeClass

# to keep backward compatibility
has_btree = 1


class ReplaceableWrapper:
    """ a wrapper around an object to make it replaceable """

    def __init__(self, ob):
        self.__ob = ob

    def __getattr__(self, name):
        if name == '__replaceable__':
            return REPLACEABLE
        return getattr(self.__ob, name)


@implementer(IOrderedContainer)
class BaseBTreeFolder(OrderedBTreeFolderBase, BaseFolder):
    """ a base class for btree-based folders supporting ordering """

    security = ClassSecurityInfo()

    def __init__(self, oid, **kwargs):
        OrderedBTreeFolderBase.__init__(self, oid)
        BaseFolder.__init__(self, oid, **kwargs)

    def _checkId(self, id, allow_dup=0):
        OrderedBTreeFolderBase._checkId(self, id, allow_dup)
        BaseFolder._checkId(self, id, allow_dup)

    def __getitem__(self, key):
        """ Override BTreeFolder __getitem__ """
        if key in self.Schema().keys() and key[:1] != "_":  # XXX 2.2
            accessor = self.Schema()[key].getAccessor(self)
            if accessor is not None:
                return accessor()
        return super(BaseBTreeFolder, self).__getitem__(key)

    # override the version from `CMFDynamicViewFTI/browserdefault.py:72`
    __call__ = BaseFolder.__call__.im_func

    @security.protected(View)
    def index_html(self, REQUEST=None, RESPONSE=None):
        """ Special case index_html """
        if 'index_html' in self:
            return self._getOb('index_html')
        request = REQUEST
        if request is None:
            request = getattr(self, 'REQUEST', None)
        if request and 'REQUEST_METHOD' in request:
            if request.maybe_webdav_client:
                method = request['REQUEST_METHOD']
                if method == 'PUT':
                    # Very likely a WebDAV client trying to create something
                    return ReplaceableWrapper(NullResource(self, 'index_html'))
                elif method in ('GET', 'HEAD', 'POST'):
                    # Do nothing, let it go and acquire.
                    pass
                else:
                    raise AttributeError('index_html')
        # Acquire from parent
        target = aq_parent(aq_inner(self)).aq_acquire('index_html')
        return ReplaceableWrapper(aq_base(target).__of__(self))

    index_html = ComputedAttribute(index_html, 1)


InitializeClass(BaseBTreeFolder)

BaseBTreeFolderSchema = BaseBTreeFolder.schema
