#-*- coding: utf-8 -*-
#
# Created on Jan 2, 2013
#
# @author: Younes JAAIDI
#
# $Id: a530d53d87285c2f15d385feaa9b74f88ee96b2f $
#

from synthetic import synthesizeMember, synthesizeConstructor

@synthesizeMember('rule_id', contract = unicode, readOnly = True)
@synthesizeMember('payload_container', contract = unicode, readOnly = True)
@synthesizeConstructor()
class ModsecurityAuditEntryMessage:
    pass
