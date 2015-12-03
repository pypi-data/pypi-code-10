# -*- coding: utf-8 -*-
from Products.CMFCore.utils import getToolByName


def migrateTo1001(context):
    PROFILE_ID = 'profile-rer.giunta:default'
    setup_tool = getToolByName(context, 'portal_setup')
    setup_tool.runImportStepFromProfile(PROFILE_ID, 'cssregistry')
