# -*- coding: utf-8 -*-
from DateTime import DateTime
from plone.app.content.testing import PLONE_APP_CONTENT_AT_INTEGRATION_TESTING
from plone.app.content.testing import PLONE_APP_CONTENT_DX_INTEGRATION_TESTING
from plone.app.testing import login
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from plone.dexterity.fti import DexterityFTI
from plone.protect.authenticator import createToken
from plone.uuid.interfaces import IUUID
from Products.CMFCore.utils import getToolByName
from Testing.makerequest import makerequest
from zope.annotation.interfaces import IAttributeAnnotatable
from zope.interface import alsoProvides
from zope.publisher.browser import TestRequest
import json
import unittest


class BaseTest(unittest.TestCase):

    def setUp(self):
        self.portal = self.layer['portal']
        login(self.portal, TEST_USER_NAME)
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

        self.portal.invokeFactory('Document', id="page", title="page")
        self.portal.page.reindexObject()

        self.request = TestRequest(
            environ={
                'HTTP_ACCEPT_LANGUAGE': 'en',
                'REQUEST_METHOD': 'POST'
            },
            form={
                'selection': '["' + IUUID(self.portal.page) + '"]',
                '_authenticator': createToken(),
                'folder': '/'
            }
        )
        self.request.REQUEST_METHOD = 'POST'
        alsoProvides(self.request, IAttributeAnnotatable)
        self.userList = 'one,two'


class DXBaseTest(BaseTest):

    layer = PLONE_APP_CONTENT_DX_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        portal_types = getToolByName(self.portal, "portal_types")
        if 'Document' not in portal_types.objectIds():
            fti = DexterityFTI('Document')
            portal_types._setObject('Document', fti)
        super(DXBaseTest, self).setUp()


class PropertiesDXTest(DXBaseTest):

    def testEffective(self):
        from plone.app.content.browser.contents.properties import PropertiesActionView  # noqa
        self.request.form['effectiveDate'] = '1999/01/01 09:00'
        view = PropertiesActionView(self.portal.page, self.request)
        view()
        self.assertEquals(self.portal.page.effective_date,
                          DateTime('1999/01/01 09:00'))

    def testExpires(self):
        from plone.app.content.browser.contents.properties import PropertiesActionView  # noqa
        self.request.form['expirationDate'] = '1999/01/01 09:00'
        view = PropertiesActionView(self.portal.page, self.request)
        view()
        self.assertEquals(self.portal.page.expiration_date,
                          DateTime('1999/01/01 09:00'))

    def testSetDexterityExcludeFromNav(self):
        from plone.app.content.browser.contents.properties import PropertiesActionView  # noqa
        self.request.form['exclude-from-nav'] = 'yes'
        view = PropertiesActionView(self.portal.page, self.request)
        view()
        self.assertEquals(self.portal.page.exclude_from_nav, True)

    def testRights(self):
        from plone.app.content.browser.contents.properties import PropertiesActionView  # noqa
        self.request.form['copyright'] = 'foobar'
        view = PropertiesActionView(self.portal.page, self.request)
        view()
        self.assertEquals(self.portal.page.rights, 'foobar')

    def testContributors(self):
        from plone.app.content.browser.contents.properties import PropertiesActionView  # noqa
        self.request.form['contributors'] = self.userList
        view = PropertiesActionView(self.portal.page, self.request)
        view()
        self.assertEquals(self.portal.page.contributors, ('one', 'two'))

    def testCreators(self):
        from plone.app.content.browser.contents.properties import PropertiesActionView  # noqa
        self.request.form['creators'] = self.userList
        view = PropertiesActionView(self.portal.page, self.request)
        view()
        self.assertEquals(
            self.portal.page.creators,
            ('one', 'two', 'test_user_1_')
        )


class PropertiesArchetypesTest(BaseTest):
    layer = PLONE_APP_CONTENT_AT_INTEGRATION_TESTING

    def testExcludeFromNav(self):
        from plone.app.content.browser.contents.properties import PropertiesActionView  # noqa
        self.request.form['exclude-from-nav'] = 'yes'
        view = PropertiesActionView(self.portal.page, self.request)
        view()
        self.assertEquals(self.portal.page.getExcludeFromNav(), True)

    def testEffective(self):
        from plone.app.content.browser.contents.properties import PropertiesActionView  # noqa
        self.request.form['effectiveDate'] = '1999/01/01 09:00'
        view = PropertiesActionView(self.portal.page, self.request)
        view()
        self.assertEquals(
            DateTime(self.portal.page.EffectiveDate()).toZone('UTC'),
            DateTime('1999/01/01 09:00').toZone('UTC'))

    def testExpires(self):
        from plone.app.content.browser.contents.properties import PropertiesActionView  # noqa
        self.request.form['expirationDate'] = '1999/01/01 09:00'
        view = PropertiesActionView(self.portal.page, self.request)
        view()
        self.assertEquals(
            DateTime(self.portal.page.ExpirationDate()).toZone('UTC'),
            DateTime('1999/01/01 09:00').toZone('UTC'))

    def testRights(self):
        from plone.app.content.browser.contents.properties import PropertiesActionView  # noqa
        self.request.form['copyright'] = 'foobar'
        view = PropertiesActionView(self.portal.page, self.request)
        view()
        self.assertEquals(self.portal.page.Rights(), 'foobar')

    def testContributors(self):
        from plone.app.content.browser.contents.properties import PropertiesActionView  # noqa
        self.request.form['contributors'] = self.userList
        view = PropertiesActionView(self.portal.page, self.request)
        view()
        self.assertEquals(self.portal.page.Contributors(), ('one', 'two'))

    def testCreators(self):
        from plone.app.content.browser.contents.properties import PropertiesActionView  # noqa
        self.request.form['creators'] = self.userList
        view = PropertiesActionView(self.portal.page, self.request)
        view()
        self.assertEquals(self.portal.page.Creators(), ('one', 'two'))


class WorkflowTest(BaseTest):

    layer = PLONE_APP_CONTENT_DX_INTEGRATION_TESTING

    def testStateChange(self):
        from plone.app.content.browser.contents.workflow import WorkflowActionView  # noqa
        self.request.form['transition'] = 'publish'
        view = WorkflowActionView(self.portal.page, self.request)
        view()
        workflowTool = getToolByName(self.portal, "portal_workflow")
        self.assertEquals(
            workflowTool.getInfoFor(self.portal.page, 'review_state'),
            'published')


class RenameTest(BaseTest):

    layer = PLONE_APP_CONTENT_DX_INTEGRATION_TESTING

    def test_folder_rename_objects(self):
        from plone.app.content.browser.contents.rename import RenameActionView
        uid = IUUID(self.portal.page)
        self.portal.invokeFactory('Document', id='page2', title='2nd page')
        uid2 = IUUID(self.portal.page2)
        self.request.form.update({
            'UID_0': uid,
            'newid_0': 'I am UnSafe! ',
            'newtitle_0': 'New!',
            'UID_1': uid2,
            'newid_1': '. ,;new id : _! ',
            'newtitle_1': 'Newer!'
        })
        view = RenameActionView(self.portal, self.request)
        view()
        self.assertEqual(self.portal['i-am-unsafe'].title, "New!")
        self.assertEqual(self.portal['new-id-_'].title, "Newer!")

    def test_default_page_updated_on_rename_objects(self):
        from plone.app.content.browser.contents.rename import RenameActionView
        self.portal.setDefaultPage('page')
        uid = IUUID(self.portal.page)
        self.request.form.update({
            'UID_0': uid,
            'newid_0': 'page-renamed',
            'newtitle_0': 'Page'
        })
        view = RenameActionView(self.portal, self.request)
        view()
        self.assertEqual(self.portal.getDefaultPage(), 'page-renamed')


class ContextInfoTest(BaseTest):

    layer = PLONE_APP_CONTENT_DX_INTEGRATION_TESTING

    def testStateChange(self):
        from plone.app.content.browser.contents import ContextInfo
        view = ContextInfo(self.portal.page, self.request)
        result = json.loads(view())
        self.assertEquals(result['object']['Title'], 'page')
        self.assertTrue(len(result['breadcrumbs']) > 0)


class DeleteDXTest(BaseTest):
    """Verify delete behavior from the folder contents view"""

    layer = PLONE_APP_CONTENT_DX_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        login(self.portal, TEST_USER_NAME)
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

        self.portal.invokeFactory('Document', id="page", title="page")
        self.portal.page.reindexObject()

        self.env = {'HTTP_ACCEPT_LANGUAGE': 'en', 'REQUEST_METHOD': 'POST'}
        self.request = makerequest(self.layer['app']).REQUEST
        self.request.environ.update(self.env)
        self.request.form = {
            'selection': '["' + IUUID(self.portal.page) + '"]',
            '_authenticator': createToken(),
            'folder': '/'
        }
        self.request.REQUEST_METHOD = 'POST'

    def make_request(self):
        request = makerequest(self.layer['app'], environ=self.env).REQUEST
        self.request.environ.update(self.env)
        request.REQUEST_METHOD = 'POST'
        return request

    def test_delete_object(self):
        from plone.app.content.browser.contents.delete import DeleteActionView
        page_id = self.portal.page.id
        self.assertTrue(page_id in self.portal)
        view = DeleteActionView(self.portal, self.request)
        view()
        self.assertTrue(page_id not in self.portal)

    def test_delete_wrong_object_by_acquisition(self):
        page_id = self.portal.page.id
        f1 = self.portal.invokeFactory('Folder', id="f1", title="folder one")
        # created a nested page with the same id as the one at the site root
        p1 = self.portal[f1].invokeFactory(
            'Document',
            id=page_id,
            title="page"
        )
        self.assertEquals(p1, page_id)
        request2 = self.make_request()

        # both pages exist before we delete on
        for location in [self.portal, self.portal[f1]]:
            self.assertTrue(p1 in location)

        # instantiate two different views and delete the same object with each
        from plone.app.content.browser.contents.delete import DeleteActionView
        object_uuid = IUUID(self.portal[f1][p1])
        for req in [self.request, request2]:
            req.form = {
                'selection': '["{}"]'.format(object_uuid),
                '_authenticator': createToken(),
                'folder': '/{}/'.format(f1)
            }
            view = DeleteActionView(self.portal, req)
            view()

        # the root page exists, the nested one is gone
        self.assertTrue(p1 in self.portal)
        self.assertFalse(p1 in self.portal[f1])


class DeleteATTest(DeleteDXTest):

    layer = PLONE_APP_CONTENT_AT_INTEGRATION_TESTING


class RearrangeDXTest(BaseTest):
    """Verify rearrange feature from the folder contents view"""

    layer = PLONE_APP_CONTENT_DX_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        login(self.portal, TEST_USER_NAME)
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

        self.portal.invokeFactory(
            'Folder',
            id="basefolder",
            title="Folder Base"
        )
        self.bf = self.portal.basefolder
        self.bf.reindexObject()
        for idx in range(0, 5):
            newid = "f{0:}".format(idx)
            self.bf.invokeFactory(
                'Folder',
                id=newid,
                # title in reverse order
                title="Folder {0:}".format(4-idx)
            )
            self.bf[newid].reindexObject()

        self.env = {'HTTP_ACCEPT_LANGUAGE': 'en', 'REQUEST_METHOD': 'POST'}
        self.request = makerequest(self.layer['app']).REQUEST
        self.request.environ.update(self.env)
        self.request.form = {
            'selection': '["' + IUUID(self.bf) + '"]',
            '_authenticator': createToken(),
            'folder': '/basefolder'
        }
        self.request.REQUEST_METHOD = 'POST'

    def test_initial_order(self):
        # just to be sure preconditions are fine
        #
        # initial ids are forward
        # and titles are set reversed!
        self.assertEqual(
            [(c[0], c[1].Title()) for c in self.bf.contentItems()],
            [
                ('f0', 'Folder 4'),
                ('f1', 'Folder 3'),
                ('f2', 'Folder 2'),
                ('f3', 'Folder 1'),
                ('f4', 'Folder 0'),
            ]
        )

    def test_rearrange_by_title(self):
        from plone.app.content.browser.contents.rearrange import RearrangeActionView  # noqa
        self.request.form.update({
            'rearrange_on': 'sortable_title',
        })
        view = RearrangeActionView(self.bf, self.request)
        view()
        self.assertEqual(
            [(c[0], c[1].Title()) for c in self.bf.contentItems()],
            [
                ('f4', 'Folder 0'),
                ('f3', 'Folder 1'),
                ('f2', 'Folder 2'),
                ('f1', 'Folder 3'),
                ('f0', 'Folder 4'),
            ],
        )

    def test_item_order_move_to_top(self):
        from plone.app.content.browser.contents.rearrange import ItemOrderActionView  # noqa
        self.request.form.update({
            'id': 'f2',
            'delta': 'top',
        })
        view = ItemOrderActionView(self.bf, self.request)
        view()
        self.assertEqual(
            [(c[0], c[1].Title()) for c in self.bf.contentItems()],
            [
                ('f2', 'Folder 2'),
                ('f0', 'Folder 4'),
                ('f1', 'Folder 3'),
                ('f3', 'Folder 1'),
                ('f4', 'Folder 0'),
            ]
        )

    def test_item_order_move_to_bottom(self):
        from plone.app.content.browser.contents.rearrange import ItemOrderActionView  # noqa
        self.request.form.update({
            'id': 'f2',
            'delta': 'bottom',
        })
        view = ItemOrderActionView(self.bf, self.request)
        view()
        self.assertEqual(
            [(c[0], c[1].Title()) for c in self.bf.contentItems()],
            [
                ('f0', 'Folder 4'),
                ('f1', 'Folder 3'),
                ('f3', 'Folder 1'),
                ('f4', 'Folder 0'),
                ('f2', 'Folder 2'),
            ]
        )

    def test_item_order_move_by_delta(self):
        from plone.app.content.browser.contents.rearrange import ItemOrderActionView  # noqa
        self.request.form.update({
            'id': 'f2',
            'delta': '-1',
        })
        view = ItemOrderActionView(self.bf, self.request)
        view()
        self.assertEqual(
            [(c[0], c[1].Title()) for c in self.bf.contentItems()],
            [
                ('f0', 'Folder 4'),
                ('f2', 'Folder 2'),
                ('f1', 'Folder 3'),
                ('f3', 'Folder 1'),
                ('f4', 'Folder 0'),
            ]
        )


class RearrangeATTest(RearrangeDXTest):

    layer = PLONE_APP_CONTENT_AT_INTEGRATION_TESTING
