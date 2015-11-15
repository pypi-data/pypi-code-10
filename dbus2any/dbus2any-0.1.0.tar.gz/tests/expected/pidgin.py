'''
Created with dbus2any

https://github.com/hugosenari/dbus2any


This code require python-dbus

Parameters:

* pydbusclient.tpl
* /im/pidgin/purple/PurpleObject
* im.pidgin.purple.PurpleService

See also:
    http://dbus.freedesktop.org/doc/dbus-specification.html
    http://dbus.freedesktop.org/doc/dbus-python/doc/tutorial.html
'''

import dbus



class Introspectable(object):
    '''
    org.freedesktop.DBus.Introspectable

    Usage:
    ------

    Instantiate this class and access the instance members and methods

    >>> obj = Introspectable()

    '''

    def __init__(self, bus_name=None, object_path=None, interface=None, bus=None):
        '''Constructor'''
        self._dbus_interface_name = interface or "org.freedesktop.DBus.Introspectable"
        self._dbus_object_path = object_path or "/im/pidgin/purple/PurpleObject"
        self._dbus_name = bus_name or "im.pidgin.purple.PurpleService"

        bus = bus or dbus.SessionBus()
        self._dbus_object =  bus.get_object(self._dbus_name, self._dbus_object_path)
        self._dbus_interface = dbus.Interface(self._dbus_object,
            dbus_interface=self._dbus_interface_name)
        self._dbus_properties = obj = dbus.Interface(self._dbus_object,
            "org.freedesktop.DBus.Properties")

    def _get_property(self, name):
        return self._dbus_properties.Get(self._dbus_interface_name, name)

    def _set_property(self, name, val):
        return self._dbus_properties.Set(self._dbus_interface_name, name, val)

    
    def Introspect(self, *arg, **kw):
        '''
        Method (call me)
        return:
            data: STRING
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.Introspect(*arg, **kw)


class PurpleInterface(object):
    '''
    im.pidgin.purple.PurpleInterface

    Usage:
    ------

    Instantiate this class and access the instance members and methods

    >>> obj = PurpleInterface()

    '''

    def __init__(self, bus_name=None, object_path=None, interface=None, bus=None):
        '''Constructor'''
        self._dbus_interface_name = interface or "im.pidgin.purple.PurpleInterface"
        self._dbus_object_path = object_path or "/im/pidgin/purple/PurpleObject"
        self._dbus_name = bus_name or "im.pidgin.purple.PurpleService"

        bus = bus or dbus.SessionBus()
        self._dbus_object =  bus.get_object(self._dbus_name, self._dbus_object_path)
        self._dbus_interface = dbus.Interface(self._dbus_object,
            dbus_interface=self._dbus_interface_name)
        self._dbus_properties = obj = dbus.Interface(self._dbus_object,
            "org.freedesktop.DBus.Properties")

    def _get_property(self, name):
        return self._dbus_properties.Get(self._dbus_interface_name, name)

    def _set_property(self, name, val):
        return self._dbus_properties.Set(self._dbus_interface_name, name, val)

    
    def PurpleAccountsFindAny(self, *arg, **kw):
        '''
        Method (call me)
        params:
            name: STRING
            protocol: STRING
            
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleAccountsFindAny(*arg, **kw)

    def PurpleAccountsFindConnected(self, *arg, **kw):
        '''
        Method (call me)
        params:
            name: STRING
            protocol: STRING
            
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleAccountsFindConnected(*arg, **kw)

    def PurpleBlistNodeIsChat(self, *arg, **kw):
        '''
        Method (call me)
        params:
            node: INT32
            
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleBlistNodeIsChat(*arg, **kw)

    def PurpleBlistNodeIsBuddy(self, *arg, **kw):
        '''
        Method (call me)
        params:
            node: INT32
            
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleBlistNodeIsBuddy(*arg, **kw)

    def PurpleBlistNodeIsContact(self, *arg, **kw):
        '''
        Method (call me)
        params:
            node: INT32
            
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleBlistNodeIsContact(*arg, **kw)

    def PurpleBlistNodeIsGroup(self, *arg, **kw):
        '''
        Method (call me)
        params:
            node: INT32
            
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleBlistNodeIsGroup(*arg, **kw)

    def PurpleBuddyIsOnline(self, *arg, **kw):
        '''
        Method (call me)
        params:
            buddy: INT32
            
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleBuddyIsOnline(*arg, **kw)

    def PurpleBlistNodeHasFlag(self, *arg, **kw):
        '''
        Method (call me)
        params:
            node: INT32
            flags: INT32
            
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleBlistNodeHasFlag(*arg, **kw)

    def PurpleBlistNodeShouldSave(self, *arg, **kw):
        '''
        Method (call me)
        params:
            node: INT32
            
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleBlistNodeShouldSave(*arg, **kw)

    def PurpleConnectionIsConnected(self, *arg, **kw):
        '''
        Method (call me)
        params:
            connection: INT32
            
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleConnectionIsConnected(*arg, **kw)

    def PurpleConnectionIsValid(self, *arg, **kw):
        '''
        Method (call me)
        params:
            connection: INT32
            
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleConnectionIsValid(*arg, **kw)

    def PurpleConvIm(self, *arg, **kw):
        '''
        Method (call me)
        params:
            conversation: INT32
            
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleConvIm(*arg, **kw)

    def PurpleConvChat(self, *arg, **kw):
        '''
        Method (call me)
        params:
            conversation: INT32
            
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleConvChat(*arg, **kw)

    def PurpleAccountNew(self, *arg, **kw):
        '''
        Method (call me)
        params:
            username: STRING
            protocol_id: STRING
            
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleAccountNew(*arg, **kw)

    def PurpleAccountDestroy(self, *arg, **kw):
        '''
        Method (call me)
        params:
            account: INT32
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleAccountDestroy(*arg, **kw)

    def PurpleAccountConnect(self, *arg, **kw):
        '''
        Method (call me)
        params:
            account: INT32
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleAccountConnect(*arg, **kw)

    def PurpleAccountRegister(self, *arg, **kw):
        '''
        Method (call me)
        params:
            account: INT32
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleAccountRegister(*arg, **kw)

    def PurpleAccountDisconnect(self, *arg, **kw):
        '''
        Method (call me)
        params:
            account: INT32
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleAccountDisconnect(*arg, **kw)

    def PurpleAccountNotifyAdded(self, *arg, **kw):
        '''
        Method (call me)
        params:
            account: INT32
            remote_user: STRING
            id: STRING
            alias: STRING
            message: STRING
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleAccountNotifyAdded(*arg, **kw)

    def PurpleAccountRequestAdd(self, *arg, **kw):
        '''
        Method (call me)
        params:
            account: INT32
            remote_user: STRING
            id: STRING
            alias: STRING
            message: STRING
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleAccountRequestAdd(*arg, **kw)

    def PurpleAccountRequestCloseWithAccount(self, *arg, **kw):
        '''
        Method (call me)
        params:
            account: INT32
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleAccountRequestCloseWithAccount(*arg, **kw)

    def PurpleAccountRequestClose(self, *arg, **kw):
        '''
        Method (call me)
        params:
            ui_handle: INT32
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleAccountRequestClose(*arg, **kw)

    def PurpleAccountRequestChangePassword(self, *arg, **kw):
        '''
        Method (call me)
        params:
            account: INT32
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleAccountRequestChangePassword(*arg, **kw)

    def PurpleAccountRequestChangeUserInfo(self, *arg, **kw):
        '''
        Method (call me)
        params:
            account: INT32
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleAccountRequestChangeUserInfo(*arg, **kw)

    def PurpleAccountSetUsername(self, *arg, **kw):
        '''
        Method (call me)
        params:
            account: INT32
            username: STRING
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleAccountSetUsername(*arg, **kw)

    def PurpleAccountSetPassword(self, *arg, **kw):
        '''
        Method (call me)
        params:
            account: INT32
            password: STRING
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleAccountSetPassword(*arg, **kw)

    def PurpleAccountSetAlias(self, *arg, **kw):
        '''
        Method (call me)
        params:
            account: INT32
            alias: STRING
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleAccountSetAlias(*arg, **kw)

    def PurpleAccountSetUserInfo(self, *arg, **kw):
        '''
        Method (call me)
        params:
            account: INT32
            user_info: STRING
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleAccountSetUserInfo(*arg, **kw)

    def PurpleAccountSetBuddyIconPath(self, *arg, **kw):
        '''
        Method (call me)
        params:
            account: INT32
            path: STRING
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleAccountSetBuddyIconPath(*arg, **kw)

    def PurpleAccountSetProtocolId(self, *arg, **kw):
        '''
        Method (call me)
        params:
            account: INT32
            protocol_id: STRING
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleAccountSetProtocolId(*arg, **kw)

    def PurpleAccountSetConnection(self, *arg, **kw):
        '''
        Method (call me)
        params:
            account: INT32
            gc: INT32
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleAccountSetConnection(*arg, **kw)

    def PurpleAccountSetRememberPassword(self, *arg, **kw):
        '''
        Method (call me)
        params:
            account: INT32
            value: INT32
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleAccountSetRememberPassword(*arg, **kw)

    def PurpleAccountSetCheckMail(self, *arg, **kw):
        '''
        Method (call me)
        params:
            account: INT32
            value: INT32
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleAccountSetCheckMail(*arg, **kw)

    def PurpleAccountSetEnabled(self, *arg, **kw):
        '''
        Method (call me)
        params:
            account: INT32
            ui: STRING
            value: INT32
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleAccountSetEnabled(*arg, **kw)

    def PurpleAccountSetProxyInfo(self, *arg, **kw):
        '''
        Method (call me)
        params:
            account: INT32
            info: INT32
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleAccountSetProxyInfo(*arg, **kw)

    def PurpleAccountSetPrivacyType(self, *arg, **kw):
        '''
        Method (call me)
        params:
            account: INT32
            privacy_type: INT32
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleAccountSetPrivacyType(*arg, **kw)

    def PurpleAccountSetStatusTypes(self, *arg, **kw):
        '''
        Method (call me)
        params:
            account: INT32
            status_types: INT32
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleAccountSetStatusTypes(*arg, **kw)

    def PurpleAccountSetStatusList(self, *arg, **kw):
        '''
        Method (call me)
        params:
            account: INT32
            status_id: STRING
            active: INT32
            attrs: INT32
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleAccountSetStatusList(*arg, **kw)

    def PurpleAccountGetSilenceSuppression(self, *arg, **kw):
        '''
        Method (call me)
        params:
            account: INT32
            
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleAccountGetSilenceSuppression(*arg, **kw)

    def PurpleAccountSetSilenceSuppression(self, *arg, **kw):
        '''
        Method (call me)
        params:
            account: INT32
            value: INT32
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleAccountSetSilenceSuppression(*arg, **kw)

    def PurpleAccountClearSettings(self, *arg, **kw):
        '''
        Method (call me)
        params:
            account: INT32
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleAccountClearSettings(*arg, **kw)

    def PurpleAccountRemoveSetting(self, *arg, **kw):
        '''
        Method (call me)
        params:
            account: INT32
            setting: STRING
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleAccountRemoveSetting(*arg, **kw)

    def PurpleAccountSetInt(self, *arg, **kw):
        '''
        Method (call me)
        params:
            account: INT32
            name: STRING
            value: INT32
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleAccountSetInt(*arg, **kw)

    def PurpleAccountSetString(self, *arg, **kw):
        '''
        Method (call me)
        params:
            account: INT32
            name: STRING
            value: STRING
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleAccountSetString(*arg, **kw)

    def PurpleAccountSetBool(self, *arg, **kw):
        '''
        Method (call me)
        params:
            account: INT32
            name: STRING
            value: INT32
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleAccountSetBool(*arg, **kw)

    def PurpleAccountSetUiInt(self, *arg, **kw):
        '''
        Method (call me)
        params:
            account: INT32
            ui: STRING
            name: STRING
            value: INT32
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleAccountSetUiInt(*arg, **kw)

    def PurpleAccountSetUiString(self, *arg, **kw):
        '''
        Method (call me)
        params:
            account: INT32
            ui: STRING
            name: STRING
            value: STRING
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleAccountSetUiString(*arg, **kw)

    def PurpleAccountSetUiBool(self, *arg, **kw):
        '''
        Method (call me)
        params:
            account: INT32
            ui: STRING
            name: STRING
            value: INT32
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleAccountSetUiBool(*arg, **kw)

    def PurpleAccountIsConnected(self, *arg, **kw):
        '''
        Method (call me)
        params:
            account: INT32
            
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleAccountIsConnected(*arg, **kw)

    def PurpleAccountIsConnecting(self, *arg, **kw):
        '''
        Method (call me)
        params:
            account: INT32
            
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleAccountIsConnecting(*arg, **kw)

    def PurpleAccountIsDisconnected(self, *arg, **kw):
        '''
        Method (call me)
        params:
            account: INT32
            
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleAccountIsDisconnected(*arg, **kw)

    def PurpleAccountGetUsername(self, *arg, **kw):
        '''
        Method (call me)
        params:
            account: INT32
            
        return:
            RESULT: STRING
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleAccountGetUsername(*arg, **kw)

    def PurpleAccountGetPassword(self, *arg, **kw):
        '''
        Method (call me)
        params:
            account: INT32
            
        return:
            RESULT: STRING
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleAccountGetPassword(*arg, **kw)

    def PurpleAccountGetAlias(self, *arg, **kw):
        '''
        Method (call me)
        params:
            account: INT32
            
        return:
            RESULT: STRING
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleAccountGetAlias(*arg, **kw)

    def PurpleAccountGetUserInfo(self, *arg, **kw):
        '''
        Method (call me)
        params:
            account: INT32
            
        return:
            RESULT: STRING
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleAccountGetUserInfo(*arg, **kw)

    def PurpleAccountGetBuddyIconPath(self, *arg, **kw):
        '''
        Method (call me)
        params:
            account: INT32
            
        return:
            RESULT: STRING
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleAccountGetBuddyIconPath(*arg, **kw)

    def PurpleAccountGetProtocolId(self, *arg, **kw):
        '''
        Method (call me)
        params:
            account: INT32
            
        return:
            RESULT: STRING
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleAccountGetProtocolId(*arg, **kw)

    def PurpleAccountGetProtocolName(self, *arg, **kw):
        '''
        Method (call me)
        params:
            account: INT32
            
        return:
            RESULT: STRING
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleAccountGetProtocolName(*arg, **kw)

    def PurpleAccountGetConnection(self, *arg, **kw):
        '''
        Method (call me)
        params:
            account: INT32
            
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleAccountGetConnection(*arg, **kw)

    def PurpleAccountGetNameForDisplay(self, *arg, **kw):
        '''
        Method (call me)
        params:
            account: INT32
            
        return:
            RESULT: STRING
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleAccountGetNameForDisplay(*arg, **kw)

    def PurpleAccountGetRememberPassword(self, *arg, **kw):
        '''
        Method (call me)
        params:
            account: INT32
            
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleAccountGetRememberPassword(*arg, **kw)

    def PurpleAccountGetCheckMail(self, *arg, **kw):
        '''
        Method (call me)
        params:
            account: INT32
            
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleAccountGetCheckMail(*arg, **kw)

    def PurpleAccountGetEnabled(self, *arg, **kw):
        '''
        Method (call me)
        params:
            account: INT32
            ui: STRING
            
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleAccountGetEnabled(*arg, **kw)

    def PurpleAccountGetProxyInfo(self, *arg, **kw):
        '''
        Method (call me)
        params:
            account: INT32
            
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleAccountGetProxyInfo(*arg, **kw)

    def PurpleAccountGetPrivacyType(self, *arg, **kw):
        '''
        Method (call me)
        params:
            account: INT32
            
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleAccountGetPrivacyType(*arg, **kw)

    def PurpleAccountGetActiveStatus(self, *arg, **kw):
        '''
        Method (call me)
        params:
            account: INT32
            
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleAccountGetActiveStatus(*arg, **kw)

    def PurpleAccountGetStatus(self, *arg, **kw):
        '''
        Method (call me)
        params:
            account: INT32
            status_id: STRING
            
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleAccountGetStatus(*arg, **kw)

    def PurpleAccountGetStatusType(self, *arg, **kw):
        '''
        Method (call me)
        params:
            account: INT32
            id: STRING
            
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleAccountGetStatusType(*arg, **kw)

    def PurpleAccountGetStatusTypeWithPrimitive(self, *arg, **kw):
        '''
        Method (call me)
        params:
            account: INT32
            primitive: INT32
            
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleAccountGetStatusTypeWithPrimitive(*arg, **kw)

    def PurpleAccountGetPresence(self, *arg, **kw):
        '''
        Method (call me)
        params:
            account: INT32
            
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleAccountGetPresence(*arg, **kw)

    def PurpleAccountIsStatusActive(self, *arg, **kw):
        '''
        Method (call me)
        params:
            account: INT32
            status_id: STRING
            
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleAccountIsStatusActive(*arg, **kw)

    def PurpleAccountGetStatusTypes(self, *arg, **kw):
        '''
        Method (call me)
        params:
            account: INT32
            
        return:
            RESULT: ai
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleAccountGetStatusTypes(*arg, **kw)

    def PurpleAccountGetInt(self, *arg, **kw):
        '''
        Method (call me)
        params:
            account: INT32
            name: STRING
            default_value: INT32
            
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleAccountGetInt(*arg, **kw)

    def PurpleAccountGetString(self, *arg, **kw):
        '''
        Method (call me)
        params:
            account: INT32
            name: STRING
            default_value: STRING
            
        return:
            RESULT: STRING
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleAccountGetString(*arg, **kw)

    def PurpleAccountGetBool(self, *arg, **kw):
        '''
        Method (call me)
        params:
            account: INT32
            name: STRING
            default_value: INT32
            
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleAccountGetBool(*arg, **kw)

    def PurpleAccountGetUiInt(self, *arg, **kw):
        '''
        Method (call me)
        params:
            account: INT32
            ui: STRING
            name: STRING
            default_value: INT32
            
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleAccountGetUiInt(*arg, **kw)

    def PurpleAccountGetUiString(self, *arg, **kw):
        '''
        Method (call me)
        params:
            account: INT32
            ui: STRING
            name: STRING
            default_value: STRING
            
        return:
            RESULT: STRING
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleAccountGetUiString(*arg, **kw)

    def PurpleAccountGetUiBool(self, *arg, **kw):
        '''
        Method (call me)
        params:
            account: INT32
            ui: STRING
            name: STRING
            default_value: INT32
            
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleAccountGetUiBool(*arg, **kw)

    def PurpleAccountGetLog(self, *arg, **kw):
        '''
        Method (call me)
        params:
            account: INT32
            create: INT32
            
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleAccountGetLog(*arg, **kw)

    def PurpleAccountDestroyLog(self, *arg, **kw):
        '''
        Method (call me)
        params:
            account: INT32
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleAccountDestroyLog(*arg, **kw)

    def PurpleAccountAddBuddy(self, *arg, **kw):
        '''
        Method (call me)
        params:
            account: INT32
            buddy: INT32
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleAccountAddBuddy(*arg, **kw)

    def PurpleAccountAddBuddyWithInvite(self, *arg, **kw):
        '''
        Method (call me)
        params:
            account: INT32
            buddy: INT32
            message: STRING
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleAccountAddBuddyWithInvite(*arg, **kw)

    def PurpleAccountAddBuddies(self, *arg, **kw):
        '''
        Method (call me)
        params:
            account: INT32
            buddies: INT32
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleAccountAddBuddies(*arg, **kw)

    def PurpleAccountAddBuddiesWithInvite(self, *arg, **kw):
        '''
        Method (call me)
        params:
            account: INT32
            buddies: INT32
            message: STRING
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleAccountAddBuddiesWithInvite(*arg, **kw)

    def PurpleAccountRemoveBuddy(self, *arg, **kw):
        '''
        Method (call me)
        params:
            account: INT32
            buddy: INT32
            group: INT32
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleAccountRemoveBuddy(*arg, **kw)

    def PurpleAccountRemoveBuddies(self, *arg, **kw):
        '''
        Method (call me)
        params:
            account: INT32
            buddies: INT32
            groups: INT32
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleAccountRemoveBuddies(*arg, **kw)

    def PurpleAccountRemoveGroup(self, *arg, **kw):
        '''
        Method (call me)
        params:
            account: INT32
            group: INT32
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleAccountRemoveGroup(*arg, **kw)

    def PurpleAccountChangePassword(self, *arg, **kw):
        '''
        Method (call me)
        params:
            account: INT32
            orig_pw: STRING
            new_pw: STRING
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleAccountChangePassword(*arg, **kw)

    def PurpleAccountSupportsOfflineMessage(self, *arg, **kw):
        '''
        Method (call me)
        params:
            account: INT32
            buddy: INT32
            
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleAccountSupportsOfflineMessage(*arg, **kw)

    def PurpleAccountGetCurrentError(self, *arg, **kw):
        '''
        Method (call me)
        params:
            account: INT32
            
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleAccountGetCurrentError(*arg, **kw)

    def PurpleAccountClearCurrentError(self, *arg, **kw):
        '''
        Method (call me)
        params:
            account: INT32
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleAccountClearCurrentError(*arg, **kw)

    def PurpleAccountsAdd(self, *arg, **kw):
        '''
        Method (call me)
        params:
            account: INT32
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleAccountsAdd(*arg, **kw)

    def PurpleAccountsRemove(self, *arg, **kw):
        '''
        Method (call me)
        params:
            account: INT32
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleAccountsRemove(*arg, **kw)

    def PurpleAccountsDelete(self, *arg, **kw):
        '''
        Method (call me)
        params:
            account: INT32
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleAccountsDelete(*arg, **kw)

    def PurpleAccountsReorder(self, *arg, **kw):
        '''
        Method (call me)
        params:
            account: INT32
            new_index: INT32
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleAccountsReorder(*arg, **kw)

    def PurpleAccountsGetAll(self, *arg, **kw):
        '''
        Method (call me)
        return:
            RESULT: ai
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleAccountsGetAll(*arg, **kw)

    def PurpleAccountsGetAllActive(self, *arg, **kw):
        '''
        Method (call me)
        return:
            RESULT: ai
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleAccountsGetAllActive(*arg, **kw)

    def PurpleAccountsFind(self, *arg, **kw):
        '''
        Method (call me)
        params:
            name: STRING
            protocol: STRING
            
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleAccountsFind(*arg, **kw)

    def PurpleAccountsRestoreCurrentStatuses(self, *arg, **kw):
        '''
        Method (call me)
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleAccountsRestoreCurrentStatuses(*arg, **kw)

    def PurpleAccountsSetUiOps(self, *arg, **kw):
        '''
        Method (call me)
        params:
            ops: INT32
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleAccountsSetUiOps(*arg, **kw)

    def PurpleAccountsGetUiOps(self, *arg, **kw):
        '''
        Method (call me)
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleAccountsGetUiOps(*arg, **kw)

    def PurpleAccountsInit(self, *arg, **kw):
        '''
        Method (call me)
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleAccountsInit(*arg, **kw)

    def PurpleAccountsUninit(self, *arg, **kw):
        '''
        Method (call me)
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleAccountsUninit(*arg, **kw)

    def PurpleBlistNew(self, *arg, **kw):
        '''
        Method (call me)
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleBlistNew(*arg, **kw)

    def PurpleSetBlist(self, *arg, **kw):
        '''
        Method (call me)
        params:
            blist: INT32
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleSetBlist(*arg, **kw)

    def PurpleGetBlist(self, *arg, **kw):
        '''
        Method (call me)
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleGetBlist(*arg, **kw)

    def PurpleBlistGetRoot(self, *arg, **kw):
        '''
        Method (call me)
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleBlistGetRoot(*arg, **kw)

    def PurpleBlistGetBuddies(self, *arg, **kw):
        '''
        Method (call me)
        return:
            RESULT: ai
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleBlistGetBuddies(*arg, **kw)

    def PurpleBlistNodeNext(self, *arg, **kw):
        '''
        Method (call me)
        params:
            node: INT32
            offline: INT32
            
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleBlistNodeNext(*arg, **kw)

    def PurpleBlistNodeGetParent(self, *arg, **kw):
        '''
        Method (call me)
        params:
            node: INT32
            
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleBlistNodeGetParent(*arg, **kw)

    def PurpleBlistNodeGetFirstChild(self, *arg, **kw):
        '''
        Method (call me)
        params:
            node: INT32
            
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleBlistNodeGetFirstChild(*arg, **kw)

    def PurpleBlistNodeGetSiblingNext(self, *arg, **kw):
        '''
        Method (call me)
        params:
            node: INT32
            
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleBlistNodeGetSiblingNext(*arg, **kw)

    def PurpleBlistNodeGetSiblingPrev(self, *arg, **kw):
        '''
        Method (call me)
        params:
            node: INT32
            
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleBlistNodeGetSiblingPrev(*arg, **kw)

    def PurpleBlistShow(self, *arg, **kw):
        '''
        Method (call me)
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleBlistShow(*arg, **kw)

    def PurpleBlistDestroy(self, *arg, **kw):
        '''
        Method (call me)
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleBlistDestroy(*arg, **kw)

    def PurpleBlistSetVisible(self, *arg, **kw):
        '''
        Method (call me)
        params:
            show: INT32
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleBlistSetVisible(*arg, **kw)

    def PurpleBlistUpdateBuddyStatus(self, *arg, **kw):
        '''
        Method (call me)
        params:
            buddy: INT32
            old_status: INT32
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleBlistUpdateBuddyStatus(*arg, **kw)

    def PurpleBlistUpdateNodeIcon(self, *arg, **kw):
        '''
        Method (call me)
        params:
            node: INT32
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleBlistUpdateNodeIcon(*arg, **kw)

    def PurpleBlistUpdateBuddyIcon(self, *arg, **kw):
        '''
        Method (call me)
        params:
            buddy: INT32
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleBlistUpdateBuddyIcon(*arg, **kw)

    def PurpleBlistRenameBuddy(self, *arg, **kw):
        '''
        Method (call me)
        params:
            buddy: INT32
            name: STRING
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleBlistRenameBuddy(*arg, **kw)

    def PurpleBlistAliasContact(self, *arg, **kw):
        '''
        Method (call me)
        params:
            contact: INT32
            alias: STRING
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleBlistAliasContact(*arg, **kw)

    def PurpleBlistAliasBuddy(self, *arg, **kw):
        '''
        Method (call me)
        params:
            buddy: INT32
            alias: STRING
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleBlistAliasBuddy(*arg, **kw)

    def PurpleBlistServerAliasBuddy(self, *arg, **kw):
        '''
        Method (call me)
        params:
            buddy: INT32
            alias: STRING
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleBlistServerAliasBuddy(*arg, **kw)

    def PurpleBlistAliasChat(self, *arg, **kw):
        '''
        Method (call me)
        params:
            chat: INT32
            alias: STRING
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleBlistAliasChat(*arg, **kw)

    def PurpleBlistRenameGroup(self, *arg, **kw):
        '''
        Method (call me)
        params:
            group: INT32
            name: STRING
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleBlistRenameGroup(*arg, **kw)

    def PurpleChatNew(self, *arg, **kw):
        '''
        Method (call me)
        params:
            account: INT32
            alias: STRING
            components: a{ss}
            
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleChatNew(*arg, **kw)

    def PurpleChatDestroy(self, *arg, **kw):
        '''
        Method (call me)
        params:
            chat: INT32
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleChatDestroy(*arg, **kw)

    def PurpleBlistAddChat(self, *arg, **kw):
        '''
        Method (call me)
        params:
            chat: INT32
            group: INT32
            node: INT32
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleBlistAddChat(*arg, **kw)

    def PurpleBuddyNew(self, *arg, **kw):
        '''
        Method (call me)
        params:
            account: INT32
            name: STRING
            alias: STRING
            
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleBuddyNew(*arg, **kw)

    def PurpleBuddyDestroy(self, *arg, **kw):
        '''
        Method (call me)
        params:
            buddy: INT32
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleBuddyDestroy(*arg, **kw)

    def PurpleBuddySetIcon(self, *arg, **kw):
        '''
        Method (call me)
        params:
            buddy: INT32
            icon: INT32
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleBuddySetIcon(*arg, **kw)

    def PurpleBuddyGetAccount(self, *arg, **kw):
        '''
        Method (call me)
        params:
            buddy: INT32
            
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleBuddyGetAccount(*arg, **kw)

    def PurpleBuddyGetName(self, *arg, **kw):
        '''
        Method (call me)
        params:
            buddy: INT32
            
        return:
            RESULT: STRING
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleBuddyGetName(*arg, **kw)

    def PurpleBuddyGetIcon(self, *arg, **kw):
        '''
        Method (call me)
        params:
            buddy: INT32
            
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleBuddyGetIcon(*arg, **kw)

    def PurpleBuddyGetContact(self, *arg, **kw):
        '''
        Method (call me)
        params:
            buddy: INT32
            
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleBuddyGetContact(*arg, **kw)

    def PurpleBuddyGetPresence(self, *arg, **kw):
        '''
        Method (call me)
        params:
            buddy: INT32
            
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleBuddyGetPresence(*arg, **kw)

    def PurpleBuddyGetMediaCaps(self, *arg, **kw):
        '''
        Method (call me)
        params:
            buddy: INT32
            
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleBuddyGetMediaCaps(*arg, **kw)

    def PurpleBuddySetMediaCaps(self, *arg, **kw):
        '''
        Method (call me)
        params:
            buddy: INT32
            media_caps: INT32
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleBuddySetMediaCaps(*arg, **kw)

    def PurpleBlistAddBuddy(self, *arg, **kw):
        '''
        Method (call me)
        params:
            buddy: INT32
            contact: INT32
            group: INT32
            node: INT32
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleBlistAddBuddy(*arg, **kw)

    def PurpleGroupNew(self, *arg, **kw):
        '''
        Method (call me)
        params:
            name: STRING
            
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleGroupNew(*arg, **kw)

    def PurpleGroupDestroy(self, *arg, **kw):
        '''
        Method (call me)
        params:
            group: INT32
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleGroupDestroy(*arg, **kw)

    def PurpleBlistAddGroup(self, *arg, **kw):
        '''
        Method (call me)
        params:
            group: INT32
            node: INT32
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleBlistAddGroup(*arg, **kw)

    def PurpleContactNew(self, *arg, **kw):
        '''
        Method (call me)
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleContactNew(*arg, **kw)

    def PurpleContactDestroy(self, *arg, **kw):
        '''
        Method (call me)
        params:
            contact: INT32
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleContactDestroy(*arg, **kw)

    def PurpleContactGetGroup(self, *arg, **kw):
        '''
        Method (call me)
        params:
            contact: INT32
            
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleContactGetGroup(*arg, **kw)

    def PurpleBlistAddContact(self, *arg, **kw):
        '''
        Method (call me)
        params:
            contact: INT32
            group: INT32
            node: INT32
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleBlistAddContact(*arg, **kw)

    def PurpleBlistMergeContact(self, *arg, **kw):
        '''
        Method (call me)
        params:
            source: INT32
            node: INT32
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleBlistMergeContact(*arg, **kw)

    def PurpleContactGetPriorityBuddy(self, *arg, **kw):
        '''
        Method (call me)
        params:
            contact: INT32
            
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleContactGetPriorityBuddy(*arg, **kw)

    def PurpleContactSetAlias(self, *arg, **kw):
        '''
        Method (call me)
        params:
            contact: INT32
            alias: STRING
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleContactSetAlias(*arg, **kw)

    def PurpleContactGetAlias(self, *arg, **kw):
        '''
        Method (call me)
        params:
            contact: INT32
            
        return:
            RESULT: STRING
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleContactGetAlias(*arg, **kw)

    def PurpleContactOnAccount(self, *arg, **kw):
        '''
        Method (call me)
        params:
            contact: INT32
            account: INT32
            
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleContactOnAccount(*arg, **kw)

    def PurpleContactInvalidatePriorityBuddy(self, *arg, **kw):
        '''
        Method (call me)
        params:
            contact: INT32
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleContactInvalidatePriorityBuddy(*arg, **kw)

    def PurpleBlistRemoveBuddy(self, *arg, **kw):
        '''
        Method (call me)
        params:
            buddy: INT32
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleBlistRemoveBuddy(*arg, **kw)

    def PurpleBlistRemoveContact(self, *arg, **kw):
        '''
        Method (call me)
        params:
            contact: INT32
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleBlistRemoveContact(*arg, **kw)

    def PurpleBlistRemoveChat(self, *arg, **kw):
        '''
        Method (call me)
        params:
            chat: INT32
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleBlistRemoveChat(*arg, **kw)

    def PurpleBlistRemoveGroup(self, *arg, **kw):
        '''
        Method (call me)
        params:
            group: INT32
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleBlistRemoveGroup(*arg, **kw)

    def PurpleBuddyGetAliasOnly(self, *arg, **kw):
        '''
        Method (call me)
        params:
            buddy: INT32
            
        return:
            RESULT: STRING
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleBuddyGetAliasOnly(*arg, **kw)

    def PurpleBuddyGetServerAlias(self, *arg, **kw):
        '''
        Method (call me)
        params:
            buddy: INT32
            
        return:
            RESULT: STRING
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleBuddyGetServerAlias(*arg, **kw)

    def PurpleBuddyGetContactAlias(self, *arg, **kw):
        '''
        Method (call me)
        params:
            buddy: INT32
            
        return:
            RESULT: STRING
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleBuddyGetContactAlias(*arg, **kw)

    def PurpleBuddyGetLocalAlias(self, *arg, **kw):
        '''
        Method (call me)
        params:
            buddy: INT32
            
        return:
            RESULT: STRING
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleBuddyGetLocalAlias(*arg, **kw)

    def PurpleBuddyGetAlias(self, *arg, **kw):
        '''
        Method (call me)
        params:
            buddy: INT32
            
        return:
            RESULT: STRING
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleBuddyGetAlias(*arg, **kw)

    def PurpleBuddyGetLocalBuddyAlias(self, *arg, **kw):
        '''
        Method (call me)
        params:
            buddy: INT32
            
        return:
            RESULT: STRING
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleBuddyGetLocalBuddyAlias(*arg, **kw)

    def PurpleChatGetName(self, *arg, **kw):
        '''
        Method (call me)
        params:
            chat: INT32
            
        return:
            RESULT: STRING
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleChatGetName(*arg, **kw)

    def PurpleFindBuddy(self, *arg, **kw):
        '''
        Method (call me)
        params:
            account: INT32
            name: STRING
            
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleFindBuddy(*arg, **kw)

    def PurpleFindBuddyInGroup(self, *arg, **kw):
        '''
        Method (call me)
        params:
            account: INT32
            name: STRING
            group: INT32
            
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleFindBuddyInGroup(*arg, **kw)

    def PurpleFindBuddies(self, *arg, **kw):
        '''
        Method (call me)
        params:
            account: INT32
            name: STRING
            
        return:
            RESULT: ai
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleFindBuddies(*arg, **kw)

    def PurpleFindGroup(self, *arg, **kw):
        '''
        Method (call me)
        params:
            name: STRING
            
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleFindGroup(*arg, **kw)

    def PurpleBlistFindChat(self, *arg, **kw):
        '''
        Method (call me)
        params:
            account: INT32
            name: STRING
            
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleBlistFindChat(*arg, **kw)

    def PurpleChatGetGroup(self, *arg, **kw):
        '''
        Method (call me)
        params:
            chat: INT32
            
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleChatGetGroup(*arg, **kw)

    def PurpleChatGetAccount(self, *arg, **kw):
        '''
        Method (call me)
        params:
            chat: INT32
            
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleChatGetAccount(*arg, **kw)

    def PurpleBuddyGetGroup(self, *arg, **kw):
        '''
        Method (call me)
        params:
            buddy: INT32
            
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleBuddyGetGroup(*arg, **kw)

    def PurpleGroupGetAccounts(self, *arg, **kw):
        '''
        Method (call me)
        params:
            g: INT32
            
        return:
            RESULT: ai
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleGroupGetAccounts(*arg, **kw)

    def PurpleGroupOnAccount(self, *arg, **kw):
        '''
        Method (call me)
        params:
            g: INT32
            account: INT32
            
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleGroupOnAccount(*arg, **kw)

    def PurpleGroupGetName(self, *arg, **kw):
        '''
        Method (call me)
        params:
            group: INT32
            
        return:
            RESULT: STRING
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleGroupGetName(*arg, **kw)

    def PurpleBlistAddAccount(self, *arg, **kw):
        '''
        Method (call me)
        params:
            account: INT32
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleBlistAddAccount(*arg, **kw)

    def PurpleBlistRemoveAccount(self, *arg, **kw):
        '''
        Method (call me)
        params:
            account: INT32
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleBlistRemoveAccount(*arg, **kw)

    def PurpleBlistGetGroupSize(self, *arg, **kw):
        '''
        Method (call me)
        params:
            group: INT32
            offline: INT32
            
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleBlistGetGroupSize(*arg, **kw)

    def PurpleBlistGetGroupOnlineCount(self, *arg, **kw):
        '''
        Method (call me)
        params:
            group: INT32
            
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleBlistGetGroupOnlineCount(*arg, **kw)

    def PurpleBlistLoad(self, *arg, **kw):
        '''
        Method (call me)
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleBlistLoad(*arg, **kw)

    def PurpleBlistScheduleSave(self, *arg, **kw):
        '''
        Method (call me)
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleBlistScheduleSave(*arg, **kw)

    def PurpleBlistRequestAddBuddy(self, *arg, **kw):
        '''
        Method (call me)
        params:
            account: INT32
            username: STRING
            group: STRING
            alias: STRING
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleBlistRequestAddBuddy(*arg, **kw)

    def PurpleBlistRequestAddChat(self, *arg, **kw):
        '''
        Method (call me)
        params:
            account: INT32
            group: INT32
            alias: STRING
            name: STRING
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleBlistRequestAddChat(*arg, **kw)

    def PurpleBlistRequestAddGroup(self, *arg, **kw):
        '''
        Method (call me)
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleBlistRequestAddGroup(*arg, **kw)

    def PurpleBlistNodeSetBool(self, *arg, **kw):
        '''
        Method (call me)
        params:
            node: INT32
            key: STRING
            value: INT32
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleBlistNodeSetBool(*arg, **kw)

    def PurpleBlistNodeGetBool(self, *arg, **kw):
        '''
        Method (call me)
        params:
            node: INT32
            key: STRING
            
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleBlistNodeGetBool(*arg, **kw)

    def PurpleBlistNodeSetInt(self, *arg, **kw):
        '''
        Method (call me)
        params:
            node: INT32
            key: STRING
            value: INT32
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleBlistNodeSetInt(*arg, **kw)

    def PurpleBlistNodeGetInt(self, *arg, **kw):
        '''
        Method (call me)
        params:
            node: INT32
            key: STRING
            
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleBlistNodeGetInt(*arg, **kw)

    def PurpleBlistNodeSetString(self, *arg, **kw):
        '''
        Method (call me)
        params:
            node: INT32
            key: STRING
            value: STRING
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleBlistNodeSetString(*arg, **kw)

    def PurpleBlistNodeGetString(self, *arg, **kw):
        '''
        Method (call me)
        params:
            node: INT32
            key: STRING
            
        return:
            RESULT: STRING
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleBlistNodeGetString(*arg, **kw)

    def PurpleBlistNodeRemoveSetting(self, *arg, **kw):
        '''
        Method (call me)
        params:
            node: INT32
            key: STRING
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleBlistNodeRemoveSetting(*arg, **kw)

    def PurpleBlistNodeSetFlags(self, *arg, **kw):
        '''
        Method (call me)
        params:
            node: INT32
            flags: INT32
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleBlistNodeSetFlags(*arg, **kw)

    def PurpleBlistNodeGetFlags(self, *arg, **kw):
        '''
        Method (call me)
        params:
            node: INT32
            
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleBlistNodeGetFlags(*arg, **kw)

    def PurpleBlistNodeGetType(self, *arg, **kw):
        '''
        Method (call me)
        params:
            node: INT32
            
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleBlistNodeGetType(*arg, **kw)

    def PurpleBlistNodeGetExtendedMenu(self, *arg, **kw):
        '''
        Method (call me)
        params:
            n: INT32
            
        return:
            RESULT: ai
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleBlistNodeGetExtendedMenu(*arg, **kw)

    def PurpleBlistSetUiOps(self, *arg, **kw):
        '''
        Method (call me)
        params:
            ops: INT32
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleBlistSetUiOps(*arg, **kw)

    def PurpleBlistGetUiOps(self, *arg, **kw):
        '''
        Method (call me)
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleBlistGetUiOps(*arg, **kw)

    def PurpleBlistInit(self, *arg, **kw):
        '''
        Method (call me)
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleBlistInit(*arg, **kw)

    def PurpleBlistUninit(self, *arg, **kw):
        '''
        Method (call me)
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleBlistUninit(*arg, **kw)

    def PurpleBuddyIconNew(self, *arg, **kw):
        '''
        Method (call me)
        params:
            account: INT32
            username: STRING
            icon_data: INT32
            icon_len: INT32
            checksum: STRING
            
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleBuddyIconNew(*arg, **kw)

    def PurpleBuddyIconRef(self, *arg, **kw):
        '''
        Method (call me)
        params:
            icon: INT32
            
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleBuddyIconRef(*arg, **kw)

    def PurpleBuddyIconUnref(self, *arg, **kw):
        '''
        Method (call me)
        params:
            icon: INT32
            
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleBuddyIconUnref(*arg, **kw)

    def PurpleBuddyIconUpdate(self, *arg, **kw):
        '''
        Method (call me)
        params:
            icon: INT32
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleBuddyIconUpdate(*arg, **kw)

    def PurpleBuddyIconSetData(self, *arg, **kw):
        '''
        Method (call me)
        params:
            icon: INT32
            data: INT32
            len: INT32
            checksum: STRING
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleBuddyIconSetData(*arg, **kw)

    def PurpleBuddyIconGetAccount(self, *arg, **kw):
        '''
        Method (call me)
        params:
            icon: INT32
            
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleBuddyIconGetAccount(*arg, **kw)

    def PurpleBuddyIconGetUsername(self, *arg, **kw):
        '''
        Method (call me)
        params:
            icon: INT32
            
        return:
            RESULT: STRING
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleBuddyIconGetUsername(*arg, **kw)

    def PurpleBuddyIconGetChecksum(self, *arg, **kw):
        '''
        Method (call me)
        params:
            icon: INT32
            
        return:
            RESULT: STRING
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleBuddyIconGetChecksum(*arg, **kw)

    def PurpleBuddyIconGetData(self, *arg, **kw):
        '''
        Method (call me)
        params:
            icon: INT32
            
        return:
            RESULT: ay
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleBuddyIconGetData(*arg, **kw)

    def PurpleBuddyIconGetExtension(self, *arg, **kw):
        '''
        Method (call me)
        params:
            icon: INT32
            
        return:
            RESULT: STRING
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleBuddyIconGetExtension(*arg, **kw)

    def PurpleBuddyIconGetFullPath(self, *arg, **kw):
        '''
        Method (call me)
        params:
            icon: INT32
            
        return:
            RESULT: STRING
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleBuddyIconGetFullPath(*arg, **kw)

    def PurpleBuddyIconsSetForUser(self, *arg, **kw):
        '''
        Method (call me)
        params:
            account: INT32
            username: STRING
            icon_data: INT32
            icon_len: INT32
            checksum: STRING
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleBuddyIconsSetForUser(*arg, **kw)

    def PurpleBuddyIconsFind(self, *arg, **kw):
        '''
        Method (call me)
        params:
            account: INT32
            username: STRING
            
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleBuddyIconsFind(*arg, **kw)

    def PurpleBuddyIconsFindAccountIcon(self, *arg, **kw):
        '''
        Method (call me)
        params:
            account: INT32
            
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleBuddyIconsFindAccountIcon(*arg, **kw)

    def PurpleBuddyIconsSetAccountIcon(self, *arg, **kw):
        '''
        Method (call me)
        params:
            account: INT32
            icon_data: INT32
            icon_len: INT32
            
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleBuddyIconsSetAccountIcon(*arg, **kw)

    def PurpleBuddyIconsGetAccountIconTimestamp(self, *arg, **kw):
        '''
        Method (call me)
        params:
            account: INT32
            
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleBuddyIconsGetAccountIconTimestamp(*arg, **kw)

    def PurpleBuddyIconsNodeHasCustomIcon(self, *arg, **kw):
        '''
        Method (call me)
        params:
            node: INT32
            
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleBuddyIconsNodeHasCustomIcon(*arg, **kw)

    def PurpleBuddyIconsNodeFindCustomIcon(self, *arg, **kw):
        '''
        Method (call me)
        params:
            node: INT32
            
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleBuddyIconsNodeFindCustomIcon(*arg, **kw)

    def PurpleBuddyIconsNodeSetCustomIcon(self, *arg, **kw):
        '''
        Method (call me)
        params:
            node: INT32
            icon_data: INT32
            icon_len: INT32
            
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleBuddyIconsNodeSetCustomIcon(*arg, **kw)

    def PurpleBuddyIconsNodeSetCustomIconFromFile(self, *arg, **kw):
        '''
        Method (call me)
        params:
            node: INT32
            filename: STRING
            
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleBuddyIconsNodeSetCustomIconFromFile(*arg, **kw)

    def PurpleBuddyIconsHasCustomIcon(self, *arg, **kw):
        '''
        Method (call me)
        params:
            contact: INT32
            
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleBuddyIconsHasCustomIcon(*arg, **kw)

    def PurpleBuddyIconsFindCustomIcon(self, *arg, **kw):
        '''
        Method (call me)
        params:
            contact: INT32
            
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleBuddyIconsFindCustomIcon(*arg, **kw)

    def PurpleBuddyIconsSetCustomIcon(self, *arg, **kw):
        '''
        Method (call me)
        params:
            contact: INT32
            icon_data: INT32
            icon_len: INT32
            
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleBuddyIconsSetCustomIcon(*arg, **kw)

    def PurpleBuddyIconsSetCaching(self, *arg, **kw):
        '''
        Method (call me)
        params:
            caching: INT32
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleBuddyIconsSetCaching(*arg, **kw)

    def PurpleBuddyIconsIsCaching(self, *arg, **kw):
        '''
        Method (call me)
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleBuddyIconsIsCaching(*arg, **kw)

    def PurpleBuddyIconsSetCacheDir(self, *arg, **kw):
        '''
        Method (call me)
        params:
            cache_dir: STRING
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleBuddyIconsSetCacheDir(*arg, **kw)

    def PurpleBuddyIconsGetCacheDir(self, *arg, **kw):
        '''
        Method (call me)
        return:
            RESULT: STRING
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleBuddyIconsGetCacheDir(*arg, **kw)

    def PurpleBuddyIconsInit(self, *arg, **kw):
        '''
        Method (call me)
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleBuddyIconsInit(*arg, **kw)

    def PurpleBuddyIconsUninit(self, *arg, **kw):
        '''
        Method (call me)
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleBuddyIconsUninit(*arg, **kw)

    def PurpleBuddyIconGetScaleSize(self, *arg, **kw):
        '''
        Method (call me)
        params:
            spec: INT32
            width: INT32
            height: INT32
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleBuddyIconGetScaleSize(*arg, **kw)

    def PurpleConnectionNew(self, *arg, **kw):
        '''
        Method (call me)
        params:
            account: INT32
            regist: INT32
            password: STRING
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleConnectionNew(*arg, **kw)

    def PurpleConnectionDestroy(self, *arg, **kw):
        '''
        Method (call me)
        params:
            gc: INT32
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleConnectionDestroy(*arg, **kw)

    def PurpleConnectionSetState(self, *arg, **kw):
        '''
        Method (call me)
        params:
            gc: INT32
            state: INT32
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleConnectionSetState(*arg, **kw)

    def PurpleConnectionSetAccount(self, *arg, **kw):
        '''
        Method (call me)
        params:
            gc: INT32
            account: INT32
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleConnectionSetAccount(*arg, **kw)

    def PurpleConnectionSetDisplayName(self, *arg, **kw):
        '''
        Method (call me)
        params:
            gc: INT32
            name: STRING
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleConnectionSetDisplayName(*arg, **kw)

    def PurpleConnectionSetProtocolData(self, *arg, **kw):
        '''
        Method (call me)
        params:
            connection: INT32
            proto_data: INT32
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleConnectionSetProtocolData(*arg, **kw)

    def PurpleConnectionGetState(self, *arg, **kw):
        '''
        Method (call me)
        params:
            gc: INT32
            
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleConnectionGetState(*arg, **kw)

    def PurpleConnectionGetAccount(self, *arg, **kw):
        '''
        Method (call me)
        params:
            gc: INT32
            
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleConnectionGetAccount(*arg, **kw)

    def PurpleConnectionGetPrpl(self, *arg, **kw):
        '''
        Method (call me)
        params:
            gc: INT32
            
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleConnectionGetPrpl(*arg, **kw)

    def PurpleConnectionGetPassword(self, *arg, **kw):
        '''
        Method (call me)
        params:
            gc: INT32
            
        return:
            RESULT: STRING
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleConnectionGetPassword(*arg, **kw)

    def PurpleConnectionGetDisplayName(self, *arg, **kw):
        '''
        Method (call me)
        params:
            gc: INT32
            
        return:
            RESULT: STRING
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleConnectionGetDisplayName(*arg, **kw)

    def PurpleConnectionUpdateProgress(self, *arg, **kw):
        '''
        Method (call me)
        params:
            gc: INT32
            text: STRING
            step: INT32
            count: INT32
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleConnectionUpdateProgress(*arg, **kw)

    def PurpleConnectionNotice(self, *arg, **kw):
        '''
        Method (call me)
        params:
            gc: INT32
            text: STRING
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleConnectionNotice(*arg, **kw)

    def PurpleConnectionError(self, *arg, **kw):
        '''
        Method (call me)
        params:
            gc: INT32
            reason: STRING
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleConnectionError(*arg, **kw)

    def PurpleConnectionErrorReason(self, *arg, **kw):
        '''
        Method (call me)
        params:
            gc: INT32
            reason: INT32
            description: STRING
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleConnectionErrorReason(*arg, **kw)

    def PurpleConnectionSslError(self, *arg, **kw):
        '''
        Method (call me)
        params:
            gc: INT32
            ssl_error: INT32
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleConnectionSslError(*arg, **kw)

    def PurpleConnectionErrorIsFatal(self, *arg, **kw):
        '''
        Method (call me)
        params:
            reason: INT32
            
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleConnectionErrorIsFatal(*arg, **kw)

    def PurpleConnectionsDisconnectAll(self, *arg, **kw):
        '''
        Method (call me)
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleConnectionsDisconnectAll(*arg, **kw)

    def PurpleConnectionsGetAll(self, *arg, **kw):
        '''
        Method (call me)
        return:
            RESULT: ai
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleConnectionsGetAll(*arg, **kw)

    def PurpleConnectionsGetConnecting(self, *arg, **kw):
        '''
        Method (call me)
        return:
            RESULT: ai
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleConnectionsGetConnecting(*arg, **kw)

    def PurpleConnectionsSetUiOps(self, *arg, **kw):
        '''
        Method (call me)
        params:
            ops: INT32
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleConnectionsSetUiOps(*arg, **kw)

    def PurpleConnectionsGetUiOps(self, *arg, **kw):
        '''
        Method (call me)
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleConnectionsGetUiOps(*arg, **kw)

    def PurpleConnectionsInit(self, *arg, **kw):
        '''
        Method (call me)
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleConnectionsInit(*arg, **kw)

    def PurpleConnectionsUninit(self, *arg, **kw):
        '''
        Method (call me)
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleConnectionsUninit(*arg, **kw)

    def PurpleConversationNew(self, *arg, **kw):
        '''
        Method (call me)
        params:
            type: INT32
            account: INT32
            name: STRING
            
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleConversationNew(*arg, **kw)

    def PurpleConversationDestroy(self, *arg, **kw):
        '''
        Method (call me)
        params:
            conv: INT32
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleConversationDestroy(*arg, **kw)

    def PurpleConversationPresent(self, *arg, **kw):
        '''
        Method (call me)
        params:
            conv: INT32
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleConversationPresent(*arg, **kw)

    def PurpleConversationGetType(self, *arg, **kw):
        '''
        Method (call me)
        params:
            conv: INT32
            
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleConversationGetType(*arg, **kw)

    def PurpleConversationSetUiOps(self, *arg, **kw):
        '''
        Method (call me)
        params:
            conv: INT32
            ops: INT32
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleConversationSetUiOps(*arg, **kw)

    def PurpleConversationsSetUiOps(self, *arg, **kw):
        '''
        Method (call me)
        params:
            ops: INT32
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleConversationsSetUiOps(*arg, **kw)

    def PurpleConversationGetUiOps(self, *arg, **kw):
        '''
        Method (call me)
        params:
            conv: INT32
            
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleConversationGetUiOps(*arg, **kw)

    def PurpleConversationSetAccount(self, *arg, **kw):
        '''
        Method (call me)
        params:
            conv: INT32
            account: INT32
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleConversationSetAccount(*arg, **kw)

    def PurpleConversationGetAccount(self, *arg, **kw):
        '''
        Method (call me)
        params:
            conv: INT32
            
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleConversationGetAccount(*arg, **kw)

    def PurpleConversationGetGc(self, *arg, **kw):
        '''
        Method (call me)
        params:
            conv: INT32
            
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleConversationGetGc(*arg, **kw)

    def PurpleConversationSetTitle(self, *arg, **kw):
        '''
        Method (call me)
        params:
            conv: INT32
            title: STRING
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleConversationSetTitle(*arg, **kw)

    def PurpleConversationGetTitle(self, *arg, **kw):
        '''
        Method (call me)
        params:
            conv: INT32
            
        return:
            RESULT: STRING
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleConversationGetTitle(*arg, **kw)

    def PurpleConversationAutosetTitle(self, *arg, **kw):
        '''
        Method (call me)
        params:
            conv: INT32
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleConversationAutosetTitle(*arg, **kw)

    def PurpleConversationSetName(self, *arg, **kw):
        '''
        Method (call me)
        params:
            conv: INT32
            name: STRING
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleConversationSetName(*arg, **kw)

    def PurpleConversationGetName(self, *arg, **kw):
        '''
        Method (call me)
        params:
            conv: INT32
            
        return:
            RESULT: STRING
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleConversationGetName(*arg, **kw)

    def PurpleConvChatCbGetAttribute(self, *arg, **kw):
        '''
        Method (call me)
        params:
            cb: INT32
            key: STRING
            
        return:
            RESULT: STRING
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleConvChatCbGetAttribute(*arg, **kw)

    def PurpleConvChatCbGetAttributeKeys(self, *arg, **kw):
        '''
        Method (call me)
        params:
            cb: INT32
            
        return:
            RESULT: ai
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleConvChatCbGetAttributeKeys(*arg, **kw)

    def PurpleConvChatCbSetAttribute(self, *arg, **kw):
        '''
        Method (call me)
        params:
            chat: INT32
            cb: INT32
            key: STRING
            value: STRING
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleConvChatCbSetAttribute(*arg, **kw)

    def PurpleConvChatCbSetAttributes(self, *arg, **kw):
        '''
        Method (call me)
        params:
            chat: INT32
            cb: INT32
            keys: INT32
            values: INT32
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleConvChatCbSetAttributes(*arg, **kw)

    def PurpleConversationSetLogging(self, *arg, **kw):
        '''
        Method (call me)
        params:
            conv: INT32
            log: INT32
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleConversationSetLogging(*arg, **kw)

    def PurpleConversationIsLogging(self, *arg, **kw):
        '''
        Method (call me)
        params:
            conv: INT32
            
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleConversationIsLogging(*arg, **kw)

    def PurpleConversationGetImData(self, *arg, **kw):
        '''
        Method (call me)
        params:
            conv: INT32
            
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleConversationGetImData(*arg, **kw)

    def PurpleConversationGetChatData(self, *arg, **kw):
        '''
        Method (call me)
        params:
            conv: INT32
            
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleConversationGetChatData(*arg, **kw)

    def PurpleGetConversations(self, *arg, **kw):
        '''
        Method (call me)
        return:
            RESULT: ai
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleGetConversations(*arg, **kw)

    def PurpleGetIms(self, *arg, **kw):
        '''
        Method (call me)
        return:
            RESULT: ai
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleGetIms(*arg, **kw)

    def PurpleGetChats(self, *arg, **kw):
        '''
        Method (call me)
        return:
            RESULT: ai
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleGetChats(*arg, **kw)

    def PurpleFindConversationWithAccount(self, *arg, **kw):
        '''
        Method (call me)
        params:
            type: INT32
            name: STRING
            account: INT32
            
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleFindConversationWithAccount(*arg, **kw)

    def PurpleConversationWrite(self, *arg, **kw):
        '''
        Method (call me)
        params:
            conv: INT32
            who: STRING
            message: STRING
            flags: INT32
            mtime: INT32
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleConversationWrite(*arg, **kw)

    def PurpleConversationSetFeatures(self, *arg, **kw):
        '''
        Method (call me)
        params:
            conv: INT32
            features: INT32
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleConversationSetFeatures(*arg, **kw)

    def PurpleConversationGetFeatures(self, *arg, **kw):
        '''
        Method (call me)
        params:
            conv: INT32
            
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleConversationGetFeatures(*arg, **kw)

    def PurpleConversationHasFocus(self, *arg, **kw):
        '''
        Method (call me)
        params:
            conv: INT32
            
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleConversationHasFocus(*arg, **kw)

    def PurpleConversationUpdate(self, *arg, **kw):
        '''
        Method (call me)
        params:
            conv: INT32
            type: INT32
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleConversationUpdate(*arg, **kw)

    def PurpleConversationGetMessageHistory(self, *arg, **kw):
        '''
        Method (call me)
        params:
            conv: INT32
            
        return:
            RESULT: ai
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleConversationGetMessageHistory(*arg, **kw)

    def PurpleConversationClearMessageHistory(self, *arg, **kw):
        '''
        Method (call me)
        params:
            conv: INT32
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleConversationClearMessageHistory(*arg, **kw)

    def PurpleConversationMessageGetSender(self, *arg, **kw):
        '''
        Method (call me)
        params:
            msg: INT32
            
        return:
            RESULT: STRING
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleConversationMessageGetSender(*arg, **kw)

    def PurpleConversationMessageGetMessage(self, *arg, **kw):
        '''
        Method (call me)
        params:
            msg: INT32
            
        return:
            RESULT: STRING
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleConversationMessageGetMessage(*arg, **kw)

    def PurpleConversationMessageGetFlags(self, *arg, **kw):
        '''
        Method (call me)
        params:
            msg: INT32
            
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleConversationMessageGetFlags(*arg, **kw)

    def PurpleConversationMessageGetTimestamp(self, *arg, **kw):
        '''
        Method (call me)
        params:
            msg: INT32
            
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleConversationMessageGetTimestamp(*arg, **kw)

    def PurpleConvImGetConversation(self, *arg, **kw):
        '''
        Method (call me)
        params:
            im: INT32
            
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleConvImGetConversation(*arg, **kw)

    def PurpleConvImSetIcon(self, *arg, **kw):
        '''
        Method (call me)
        params:
            im: INT32
            icon: INT32
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleConvImSetIcon(*arg, **kw)

    def PurpleConvImGetIcon(self, *arg, **kw):
        '''
        Method (call me)
        params:
            im: INT32
            
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleConvImGetIcon(*arg, **kw)

    def PurpleConvImSetTypingState(self, *arg, **kw):
        '''
        Method (call me)
        params:
            im: INT32
            state: INT32
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleConvImSetTypingState(*arg, **kw)

    def PurpleConvImGetTypingState(self, *arg, **kw):
        '''
        Method (call me)
        params:
            im: INT32
            
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleConvImGetTypingState(*arg, **kw)

    def PurpleConvImStartTypingTimeout(self, *arg, **kw):
        '''
        Method (call me)
        params:
            im: INT32
            timeout: INT32
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleConvImStartTypingTimeout(*arg, **kw)

    def PurpleConvImStopTypingTimeout(self, *arg, **kw):
        '''
        Method (call me)
        params:
            im: INT32
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleConvImStopTypingTimeout(*arg, **kw)

    def PurpleConvImGetTypingTimeout(self, *arg, **kw):
        '''
        Method (call me)
        params:
            im: INT32
            
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleConvImGetTypingTimeout(*arg, **kw)

    def PurpleConvImSetTypeAgain(self, *arg, **kw):
        '''
        Method (call me)
        params:
            im: INT32
            val: UINT32
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleConvImSetTypeAgain(*arg, **kw)

    def PurpleConvImGetTypeAgain(self, *arg, **kw):
        '''
        Method (call me)
        params:
            im: INT32
            
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleConvImGetTypeAgain(*arg, **kw)

    def PurpleConvImStartSendTypedTimeout(self, *arg, **kw):
        '''
        Method (call me)
        params:
            im: INT32
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleConvImStartSendTypedTimeout(*arg, **kw)

    def PurpleConvImStopSendTypedTimeout(self, *arg, **kw):
        '''
        Method (call me)
        params:
            im: INT32
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleConvImStopSendTypedTimeout(*arg, **kw)

    def PurpleConvImGetSendTypedTimeout(self, *arg, **kw):
        '''
        Method (call me)
        params:
            im: INT32
            
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleConvImGetSendTypedTimeout(*arg, **kw)

    def PurpleConvImUpdateTyping(self, *arg, **kw):
        '''
        Method (call me)
        params:
            im: INT32
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleConvImUpdateTyping(*arg, **kw)

    def PurpleConvImWrite(self, *arg, **kw):
        '''
        Method (call me)
        params:
            im: INT32
            who: STRING
            message: STRING
            flags: INT32
            mtime: INT32
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleConvImWrite(*arg, **kw)

    def PurpleConvPresentError(self, *arg, **kw):
        '''
        Method (call me)
        params:
            who: STRING
            account: INT32
            what: STRING
            
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleConvPresentError(*arg, **kw)

    def PurpleConvImSend(self, *arg, **kw):
        '''
        Method (call me)
        params:
            im: INT32
            message: STRING
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleConvImSend(*arg, **kw)

    def PurpleConvSendConfirm(self, *arg, **kw):
        '''
        Method (call me)
        params:
            conv: INT32
            message: STRING
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleConvSendConfirm(*arg, **kw)

    def PurpleConvImSendWithFlags(self, *arg, **kw):
        '''
        Method (call me)
        params:
            im: INT32
            message: STRING
            flags: INT32
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleConvImSendWithFlags(*arg, **kw)

    def PurpleConvCustomSmileyAdd(self, *arg, **kw):
        '''
        Method (call me)
        params:
            conv: INT32
            smile: STRING
            cksum_type: STRING
            chksum: STRING
            remote: INT32
            
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleConvCustomSmileyAdd(*arg, **kw)

    def PurpleConvCustomSmileyClose(self, *arg, **kw):
        '''
        Method (call me)
        params:
            conv: INT32
            smile: STRING
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleConvCustomSmileyClose(*arg, **kw)

    def PurpleConvChatGetConversation(self, *arg, **kw):
        '''
        Method (call me)
        params:
            chat: INT32
            
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleConvChatGetConversation(*arg, **kw)

    def PurpleConvChatSetUsers(self, *arg, **kw):
        '''
        Method (call me)
        params:
            chat: INT32
            users: INT32
            
        return:
            RESULT: ai
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleConvChatSetUsers(*arg, **kw)

    def PurpleConvChatGetUsers(self, *arg, **kw):
        '''
        Method (call me)
        params:
            chat: INT32
            
        return:
            RESULT: ai
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleConvChatGetUsers(*arg, **kw)

    def PurpleConvChatIgnore(self, *arg, **kw):
        '''
        Method (call me)
        params:
            chat: INT32
            name: STRING
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleConvChatIgnore(*arg, **kw)

    def PurpleConvChatUnignore(self, *arg, **kw):
        '''
        Method (call me)
        params:
            chat: INT32
            name: STRING
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleConvChatUnignore(*arg, **kw)

    def PurpleConvChatSetIgnored(self, *arg, **kw):
        '''
        Method (call me)
        params:
            chat: INT32
            ignored: INT32
            
        return:
            RESULT: ai
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleConvChatSetIgnored(*arg, **kw)

    def PurpleConvChatGetIgnored(self, *arg, **kw):
        '''
        Method (call me)
        params:
            chat: INT32
            
        return:
            RESULT: ai
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleConvChatGetIgnored(*arg, **kw)

    def PurpleConvChatGetIgnoredUser(self, *arg, **kw):
        '''
        Method (call me)
        params:
            chat: INT32
            user: STRING
            
        return:
            RESULT: STRING
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleConvChatGetIgnoredUser(*arg, **kw)

    def PurpleConvChatIsUserIgnored(self, *arg, **kw):
        '''
        Method (call me)
        params:
            chat: INT32
            user: STRING
            
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleConvChatIsUserIgnored(*arg, **kw)

    def PurpleConvChatSetTopic(self, *arg, **kw):
        '''
        Method (call me)
        params:
            chat: INT32
            who: STRING
            topic: STRING
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleConvChatSetTopic(*arg, **kw)

    def PurpleConvChatGetTopic(self, *arg, **kw):
        '''
        Method (call me)
        params:
            chat: INT32
            
        return:
            RESULT: STRING
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleConvChatGetTopic(*arg, **kw)

    def PurpleConvChatSetId(self, *arg, **kw):
        '''
        Method (call me)
        params:
            chat: INT32
            id: INT32
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleConvChatSetId(*arg, **kw)

    def PurpleConvChatGetId(self, *arg, **kw):
        '''
        Method (call me)
        params:
            chat: INT32
            
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleConvChatGetId(*arg, **kw)

    def PurpleConvChatWrite(self, *arg, **kw):
        '''
        Method (call me)
        params:
            chat: INT32
            who: STRING
            message: STRING
            flags: INT32
            mtime: INT32
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleConvChatWrite(*arg, **kw)

    def PurpleConvChatSend(self, *arg, **kw):
        '''
        Method (call me)
        params:
            chat: INT32
            message: STRING
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleConvChatSend(*arg, **kw)

    def PurpleConvChatSendWithFlags(self, *arg, **kw):
        '''
        Method (call me)
        params:
            chat: INT32
            message: STRING
            flags: INT32
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleConvChatSendWithFlags(*arg, **kw)

    def PurpleConvChatAddUser(self, *arg, **kw):
        '''
        Method (call me)
        params:
            chat: INT32
            user: STRING
            extra_msg: STRING
            flags: INT32
            new_arrival: INT32
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleConvChatAddUser(*arg, **kw)

    def PurpleConvChatAddUsers(self, *arg, **kw):
        '''
        Method (call me)
        params:
            chat: INT32
            users: INT32
            extra_msgs: INT32
            flags: INT32
            new_arrivals: INT32
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleConvChatAddUsers(*arg, **kw)

    def PurpleConvChatRenameUser(self, *arg, **kw):
        '''
        Method (call me)
        params:
            chat: INT32
            old_user: STRING
            new_user: STRING
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleConvChatRenameUser(*arg, **kw)

    def PurpleConvChatRemoveUser(self, *arg, **kw):
        '''
        Method (call me)
        params:
            chat: INT32
            user: STRING
            reason: STRING
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleConvChatRemoveUser(*arg, **kw)

    def PurpleConvChatRemoveUsers(self, *arg, **kw):
        '''
        Method (call me)
        params:
            chat: INT32
            users: INT32
            reason: STRING
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleConvChatRemoveUsers(*arg, **kw)

    def PurpleConvChatFindUser(self, *arg, **kw):
        '''
        Method (call me)
        params:
            chat: INT32
            user: STRING
            
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleConvChatFindUser(*arg, **kw)

    def PurpleConvChatUserSetFlags(self, *arg, **kw):
        '''
        Method (call me)
        params:
            chat: INT32
            user: STRING
            flags: INT32
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleConvChatUserSetFlags(*arg, **kw)

    def PurpleConvChatUserGetFlags(self, *arg, **kw):
        '''
        Method (call me)
        params:
            chat: INT32
            user: STRING
            
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleConvChatUserGetFlags(*arg, **kw)

    def PurpleConvChatClearUsers(self, *arg, **kw):
        '''
        Method (call me)
        params:
            chat: INT32
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleConvChatClearUsers(*arg, **kw)

    def PurpleConvChatSetNick(self, *arg, **kw):
        '''
        Method (call me)
        params:
            chat: INT32
            nick: STRING
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleConvChatSetNick(*arg, **kw)

    def PurpleConvChatGetNick(self, *arg, **kw):
        '''
        Method (call me)
        params:
            chat: INT32
            
        return:
            RESULT: STRING
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleConvChatGetNick(*arg, **kw)

    def PurpleFindChat(self, *arg, **kw):
        '''
        Method (call me)
        params:
            gc: INT32
            id: INT32
            
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleFindChat(*arg, **kw)

    def PurpleConvChatLeft(self, *arg, **kw):
        '''
        Method (call me)
        params:
            chat: INT32
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleConvChatLeft(*arg, **kw)

    def PurpleConvChatInviteUser(self, *arg, **kw):
        '''
        Method (call me)
        params:
            chat: INT32
            user: STRING
            message: STRING
            confirm: INT32
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleConvChatInviteUser(*arg, **kw)

    def PurpleConvChatHasLeft(self, *arg, **kw):
        '''
        Method (call me)
        params:
            chat: INT32
            
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleConvChatHasLeft(*arg, **kw)

    def PurpleConvChatCbNew(self, *arg, **kw):
        '''
        Method (call me)
        params:
            name: STRING
            alias: STRING
            flags: INT32
            
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleConvChatCbNew(*arg, **kw)

    def PurpleConvChatCbFind(self, *arg, **kw):
        '''
        Method (call me)
        params:
            chat: INT32
            name: STRING
            
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleConvChatCbFind(*arg, **kw)

    def PurpleConvChatCbGetName(self, *arg, **kw):
        '''
        Method (call me)
        params:
            cb: INT32
            
        return:
            RESULT: STRING
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleConvChatCbGetName(*arg, **kw)

    def PurpleConvChatCbDestroy(self, *arg, **kw):
        '''
        Method (call me)
        params:
            cb: INT32
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleConvChatCbDestroy(*arg, **kw)

    def PurpleConversationGetExtendedMenu(self, *arg, **kw):
        '''
        Method (call me)
        params:
            conv: INT32
            
        return:
            RESULT: ai
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleConversationGetExtendedMenu(*arg, **kw)

    def PurpleConversationsInit(self, *arg, **kw):
        '''
        Method (call me)
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleConversationsInit(*arg, **kw)

    def PurpleConversationsUninit(self, *arg, **kw):
        '''
        Method (call me)
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleConversationsUninit(*arg, **kw)

    def PurpleCoreInit(self, *arg, **kw):
        '''
        Method (call me)
        params:
            ui: STRING
            
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleCoreInit(*arg, **kw)

    def PurpleCoreQuit(self, *arg, **kw):
        '''
        Method (call me)
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleCoreQuit(*arg, **kw)

    def PurpleCoreGetVersion(self, *arg, **kw):
        '''
        Method (call me)
        return:
            RESULT: STRING
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleCoreGetVersion(*arg, **kw)

    def PurpleCoreGetUi(self, *arg, **kw):
        '''
        Method (call me)
        return:
            RESULT: STRING
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleCoreGetUi(*arg, **kw)

    def PurpleGetCore(self, *arg, **kw):
        '''
        Method (call me)
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleGetCore(*arg, **kw)

    def PurpleCoreSetUiOps(self, *arg, **kw):
        '''
        Method (call me)
        params:
            ops: INT32
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleCoreSetUiOps(*arg, **kw)

    def PurpleCoreGetUiOps(self, *arg, **kw):
        '''
        Method (call me)
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleCoreGetUiOps(*arg, **kw)

    def PurpleCoreMigrate(self, *arg, **kw):
        '''
        Method (call me)
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleCoreMigrate(*arg, **kw)

    def PurpleCoreEnsureSingleInstance(self, *arg, **kw):
        '''
        Method (call me)
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleCoreEnsureSingleInstance(*arg, **kw)

    def PurpleXferNew(self, *arg, **kw):
        '''
        Method (call me)
        params:
            account: INT32
            type: INT32
            who: STRING
            
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleXferNew(*arg, **kw)

    def PurpleXfersGetAll(self, *arg, **kw):
        '''
        Method (call me)
        return:
            RESULT: ai
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleXfersGetAll(*arg, **kw)

    def PurpleXferRef(self, *arg, **kw):
        '''
        Method (call me)
        params:
            xfer: INT32
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleXferRef(*arg, **kw)

    def PurpleXferUnref(self, *arg, **kw):
        '''
        Method (call me)
        params:
            xfer: INT32
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleXferUnref(*arg, **kw)

    def PurpleXferRequest(self, *arg, **kw):
        '''
        Method (call me)
        params:
            xfer: INT32
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleXferRequest(*arg, **kw)

    def PurpleXferRequestAccepted(self, *arg, **kw):
        '''
        Method (call me)
        params:
            xfer: INT32
            filename: STRING
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleXferRequestAccepted(*arg, **kw)

    def PurpleXferRequestDenied(self, *arg, **kw):
        '''
        Method (call me)
        params:
            xfer: INT32
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleXferRequestDenied(*arg, **kw)

    def PurpleXferGetType(self, *arg, **kw):
        '''
        Method (call me)
        params:
            xfer: INT32
            
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleXferGetType(*arg, **kw)

    def PurpleXferGetAccount(self, *arg, **kw):
        '''
        Method (call me)
        params:
            xfer: INT32
            
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleXferGetAccount(*arg, **kw)

    def PurpleXferGetRemoteUser(self, *arg, **kw):
        '''
        Method (call me)
        params:
            xfer: INT32
            
        return:
            RESULT: STRING
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleXferGetRemoteUser(*arg, **kw)

    def PurpleXferGetStatus(self, *arg, **kw):
        '''
        Method (call me)
        params:
            xfer: INT32
            
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleXferGetStatus(*arg, **kw)

    def PurpleXferIsCanceled(self, *arg, **kw):
        '''
        Method (call me)
        params:
            xfer: INT32
            
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleXferIsCanceled(*arg, **kw)

    def PurpleXferIsCompleted(self, *arg, **kw):
        '''
        Method (call me)
        params:
            xfer: INT32
            
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleXferIsCompleted(*arg, **kw)

    def PurpleXferGetFilename(self, *arg, **kw):
        '''
        Method (call me)
        params:
            xfer: INT32
            
        return:
            RESULT: STRING
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleXferGetFilename(*arg, **kw)

    def PurpleXferGetLocalFilename(self, *arg, **kw):
        '''
        Method (call me)
        params:
            xfer: INT32
            
        return:
            RESULT: STRING
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleXferGetLocalFilename(*arg, **kw)

    def PurpleXferGetBytesSent(self, *arg, **kw):
        '''
        Method (call me)
        params:
            xfer: INT32
            
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleXferGetBytesSent(*arg, **kw)

    def PurpleXferGetBytesRemaining(self, *arg, **kw):
        '''
        Method (call me)
        params:
            xfer: INT32
            
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleXferGetBytesRemaining(*arg, **kw)

    def PurpleXferGetSize(self, *arg, **kw):
        '''
        Method (call me)
        params:
            xfer: INT32
            
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleXferGetSize(*arg, **kw)

    def PurpleXferGetLocalPort(self, *arg, **kw):
        '''
        Method (call me)
        params:
            xfer: INT32
            
        return:
            RESULT: UINT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleXferGetLocalPort(*arg, **kw)

    def PurpleXferGetRemoteIp(self, *arg, **kw):
        '''
        Method (call me)
        params:
            xfer: INT32
            
        return:
            RESULT: STRING
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleXferGetRemoteIp(*arg, **kw)

    def PurpleXferGetRemotePort(self, *arg, **kw):
        '''
        Method (call me)
        params:
            xfer: INT32
            
        return:
            RESULT: UINT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleXferGetRemotePort(*arg, **kw)

    def PurpleXferGetStartTime(self, *arg, **kw):
        '''
        Method (call me)
        params:
            xfer: INT32
            
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleXferGetStartTime(*arg, **kw)

    def PurpleXferGetEndTime(self, *arg, **kw):
        '''
        Method (call me)
        params:
            xfer: INT32
            
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleXferGetEndTime(*arg, **kw)

    def PurpleXferSetCompleted(self, *arg, **kw):
        '''
        Method (call me)
        params:
            xfer: INT32
            completed: INT32
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleXferSetCompleted(*arg, **kw)

    def PurpleXferSetMessage(self, *arg, **kw):
        '''
        Method (call me)
        params:
            xfer: INT32
            message: STRING
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleXferSetMessage(*arg, **kw)

    def PurpleXferSetFilename(self, *arg, **kw):
        '''
        Method (call me)
        params:
            xfer: INT32
            filename: STRING
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleXferSetFilename(*arg, **kw)

    def PurpleXferSetLocalFilename(self, *arg, **kw):
        '''
        Method (call me)
        params:
            xfer: INT32
            filename: STRING
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleXferSetLocalFilename(*arg, **kw)

    def PurpleXferSetSize(self, *arg, **kw):
        '''
        Method (call me)
        params:
            xfer: INT32
            size: INT32
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleXferSetSize(*arg, **kw)

    def PurpleXferSetBytesSent(self, *arg, **kw):
        '''
        Method (call me)
        params:
            xfer: INT32
            bytes_sent: INT32
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleXferSetBytesSent(*arg, **kw)

    def PurpleXferGetUiOps(self, *arg, **kw):
        '''
        Method (call me)
        params:
            xfer: INT32
            
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleXferGetUiOps(*arg, **kw)

    def PurpleXferStart(self, *arg, **kw):
        '''
        Method (call me)
        params:
            xfer: INT32
            fd: INT32
            ip: STRING
            port: UINT32
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleXferStart(*arg, **kw)

    def PurpleXferEnd(self, *arg, **kw):
        '''
        Method (call me)
        params:
            xfer: INT32
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleXferEnd(*arg, **kw)

    def PurpleXferAdd(self, *arg, **kw):
        '''
        Method (call me)
        params:
            xfer: INT32
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleXferAdd(*arg, **kw)

    def PurpleXferCancelLocal(self, *arg, **kw):
        '''
        Method (call me)
        params:
            xfer: INT32
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleXferCancelLocal(*arg, **kw)

    def PurpleXferCancelRemote(self, *arg, **kw):
        '''
        Method (call me)
        params:
            xfer: INT32
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleXferCancelRemote(*arg, **kw)

    def PurpleXferError(self, *arg, **kw):
        '''
        Method (call me)
        params:
            type: INT32
            account: INT32
            who: STRING
            msg: STRING
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleXferError(*arg, **kw)

    def PurpleXferUpdateProgress(self, *arg, **kw):
        '''
        Method (call me)
        params:
            xfer: INT32
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleXferUpdateProgress(*arg, **kw)

    def PurpleXferGetThumbnail(self, *arg, **kw):
        '''
        Method (call me)
        params:
            xfer: INT32
            
        return:
            RESULT: ay
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleXferGetThumbnail(*arg, **kw)

    def PurpleXferGetThumbnailMimetype(self, *arg, **kw):
        '''
        Method (call me)
        params:
            xfer: INT32
            
        return:
            RESULT: STRING
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleXferGetThumbnailMimetype(*arg, **kw)

    def PurpleXferPrepareThumbnail(self, *arg, **kw):
        '''
        Method (call me)
        params:
            xfer: INT32
            formats: STRING
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleXferPrepareThumbnail(*arg, **kw)

    def PurpleXfersInit(self, *arg, **kw):
        '''
        Method (call me)
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleXfersInit(*arg, **kw)

    def PurpleXfersUninit(self, *arg, **kw):
        '''
        Method (call me)
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleXfersUninit(*arg, **kw)

    def PurpleXfersSetUiOps(self, *arg, **kw):
        '''
        Method (call me)
        params:
            ops: INT32
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleXfersSetUiOps(*arg, **kw)

    def PurpleXfersGetUiOps(self, *arg, **kw):
        '''
        Method (call me)
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleXfersGetUiOps(*arg, **kw)

    def PurpleLogFree(self, *arg, **kw):
        '''
        Method (call me)
        params:
            log: INT32
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleLogFree(*arg, **kw)

    def PurpleLogWrite(self, *arg, **kw):
        '''
        Method (call me)
        params:
            log: INT32
            type: INT32
            from: STRING
            time: INT32
            message: STRING
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleLogWrite(*arg, **kw)

    def PurpleLogGetLogs(self, *arg, **kw):
        '''
        Method (call me)
        params:
            type: INT32
            name: STRING
            account: INT32
            
        return:
            RESULT: ai
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleLogGetLogs(*arg, **kw)

    def PurpleLogGetSystemLogs(self, *arg, **kw):
        '''
        Method (call me)
        params:
            account: INT32
            
        return:
            RESULT: ai
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleLogGetSystemLogs(*arg, **kw)

    def PurpleLogGetSize(self, *arg, **kw):
        '''
        Method (call me)
        params:
            log: INT32
            
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleLogGetSize(*arg, **kw)

    def PurpleLogGetTotalSize(self, *arg, **kw):
        '''
        Method (call me)
        params:
            type: INT32
            name: STRING
            account: INT32
            
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleLogGetTotalSize(*arg, **kw)

    def PurpleLogGetActivityScore(self, *arg, **kw):
        '''
        Method (call me)
        params:
            type: INT32
            name: STRING
            account: INT32
            
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleLogGetActivityScore(*arg, **kw)

    def PurpleLogIsDeletable(self, *arg, **kw):
        '''
        Method (call me)
        params:
            log: INT32
            
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleLogIsDeletable(*arg, **kw)

    def PurpleLogDelete(self, *arg, **kw):
        '''
        Method (call me)
        params:
            log: INT32
            
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleLogDelete(*arg, **kw)

    def PurpleLogGetLogDir(self, *arg, **kw):
        '''
        Method (call me)
        params:
            type: INT32
            name: STRING
            account: INT32
            
        return:
            RESULT: STRING
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleLogGetLogDir(*arg, **kw)

    def PurpleLogSetFree(self, *arg, **kw):
        '''
        Method (call me)
        params:
            set: INT32
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleLogSetFree(*arg, **kw)

    def PurpleLogCommonWriter(self, *arg, **kw):
        '''
        Method (call me)
        params:
            log: INT32
            ext: STRING
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleLogCommonWriter(*arg, **kw)

    def PurpleLogCommonLister(self, *arg, **kw):
        '''
        Method (call me)
        params:
            type: INT32
            name: STRING
            account: INT32
            ext: STRING
            logger: INT32
            
        return:
            RESULT: ai
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleLogCommonLister(*arg, **kw)

    def PurpleLogCommonTotalSizer(self, *arg, **kw):
        '''
        Method (call me)
        params:
            type: INT32
            name: STRING
            account: INT32
            ext: STRING
            
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleLogCommonTotalSizer(*arg, **kw)

    def PurpleLogCommonSizer(self, *arg, **kw):
        '''
        Method (call me)
        params:
            log: INT32
            
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleLogCommonSizer(*arg, **kw)

    def PurpleLogCommonDeleter(self, *arg, **kw):
        '''
        Method (call me)
        params:
            log: INT32
            
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleLogCommonDeleter(*arg, **kw)

    def PurpleLogCommonIsDeletable(self, *arg, **kw):
        '''
        Method (call me)
        params:
            log: INT32
            
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleLogCommonIsDeletable(*arg, **kw)

    def PurpleLogLoggerFree(self, *arg, **kw):
        '''
        Method (call me)
        params:
            logger: INT32
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleLogLoggerFree(*arg, **kw)

    def PurpleLogLoggerAdd(self, *arg, **kw):
        '''
        Method (call me)
        params:
            logger: INT32
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleLogLoggerAdd(*arg, **kw)

    def PurpleLogLoggerRemove(self, *arg, **kw):
        '''
        Method (call me)
        params:
            logger: INT32
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleLogLoggerRemove(*arg, **kw)

    def PurpleLogLoggerSet(self, *arg, **kw):
        '''
        Method (call me)
        params:
            logger: INT32
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleLogLoggerSet(*arg, **kw)

    def PurpleLogLoggerGet(self, *arg, **kw):
        '''
        Method (call me)
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleLogLoggerGet(*arg, **kw)

    def PurpleLogLoggerGetOptions(self, *arg, **kw):
        '''
        Method (call me)
        return:
            RESULT: ai
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleLogLoggerGetOptions(*arg, **kw)

    def PurpleLogInit(self, *arg, **kw):
        '''
        Method (call me)
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleLogInit(*arg, **kw)

    def PurpleLogUninit(self, *arg, **kw):
        '''
        Method (call me)
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleLogUninit(*arg, **kw)

    def PurpleNotifySearchresultsFree(self, *arg, **kw):
        '''
        Method (call me)
        params:
            results: INT32
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleNotifySearchresultsFree(*arg, **kw)

    def PurpleNotifySearchresultsNewRows(self, *arg, **kw):
        '''
        Method (call me)
        params:
            gc: INT32
            results: INT32
            data: INT32
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleNotifySearchresultsNewRows(*arg, **kw)

    def PurpleNotifySearchresultsNew(self, *arg, **kw):
        '''
        Method (call me)
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleNotifySearchresultsNew(*arg, **kw)

    def PurpleNotifySearchresultsColumnNew(self, *arg, **kw):
        '''
        Method (call me)
        params:
            title: STRING
            
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleNotifySearchresultsColumnNew(*arg, **kw)

    def PurpleNotifySearchresultsColumnAdd(self, *arg, **kw):
        '''
        Method (call me)
        params:
            results: INT32
            column: INT32
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleNotifySearchresultsColumnAdd(*arg, **kw)

    def PurpleNotifySearchresultsRowAdd(self, *arg, **kw):
        '''
        Method (call me)
        params:
            results: INT32
            row: INT32
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleNotifySearchresultsRowAdd(*arg, **kw)

    def PurpleNotifySearchresultsGetRowsCount(self, *arg, **kw):
        '''
        Method (call me)
        params:
            results: INT32
            
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleNotifySearchresultsGetRowsCount(*arg, **kw)

    def PurpleNotifySearchresultsGetColumnsCount(self, *arg, **kw):
        '''
        Method (call me)
        params:
            results: INT32
            
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleNotifySearchresultsGetColumnsCount(*arg, **kw)

    def PurpleNotifySearchresultsRowGet(self, *arg, **kw):
        '''
        Method (call me)
        params:
            results: INT32
            row_id: UINT32
            
        return:
            RESULT: ai
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleNotifySearchresultsRowGet(*arg, **kw)

    def PurpleNotifySearchresultsColumnGetTitle(self, *arg, **kw):
        '''
        Method (call me)
        params:
            results: INT32
            column_id: UINT32
            
        return:
            RESULT: STRING
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleNotifySearchresultsColumnGetTitle(*arg, **kw)

    def PurpleNotifyUserInfoNew(self, *arg, **kw):
        '''
        Method (call me)
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleNotifyUserInfoNew(*arg, **kw)

    def PurpleNotifyUserInfoDestroy(self, *arg, **kw):
        '''
        Method (call me)
        params:
            user_info: INT32
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleNotifyUserInfoDestroy(*arg, **kw)

    def PurpleNotifyUserInfoGetEntries(self, *arg, **kw):
        '''
        Method (call me)
        params:
            user_info: INT32
            
        return:
            RESULT: ai
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleNotifyUserInfoGetEntries(*arg, **kw)

    def PurpleNotifyUserInfoGetTextWithNewline(self, *arg, **kw):
        '''
        Method (call me)
        params:
            user_info: INT32
            newline: STRING
            
        return:
            RESULT: STRING
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleNotifyUserInfoGetTextWithNewline(*arg, **kw)

    def PurpleNotifyUserInfoAddPair(self, *arg, **kw):
        '''
        Method (call me)
        params:
            user_info: INT32
            label: STRING
            value: STRING
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleNotifyUserInfoAddPair(*arg, **kw)

    def PurpleNotifyUserInfoAddPairPlaintext(self, *arg, **kw):
        '''
        Method (call me)
        params:
            user_info: INT32
            label: STRING
            value: STRING
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleNotifyUserInfoAddPairPlaintext(*arg, **kw)

    def PurpleNotifyUserInfoPrependPair(self, *arg, **kw):
        '''
        Method (call me)
        params:
            user_info: INT32
            label: STRING
            value: STRING
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleNotifyUserInfoPrependPair(*arg, **kw)

    def PurpleNotifyUserInfoRemoveEntry(self, *arg, **kw):
        '''
        Method (call me)
        params:
            user_info: INT32
            user_info_entry: INT32
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleNotifyUserInfoRemoveEntry(*arg, **kw)

    def PurpleNotifyUserInfoEntryNew(self, *arg, **kw):
        '''
        Method (call me)
        params:
            label: STRING
            value: STRING
            
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleNotifyUserInfoEntryNew(*arg, **kw)

    def PurpleNotifyUserInfoAddSectionBreak(self, *arg, **kw):
        '''
        Method (call me)
        params:
            user_info: INT32
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleNotifyUserInfoAddSectionBreak(*arg, **kw)

    def PurpleNotifyUserInfoPrependSectionBreak(self, *arg, **kw):
        '''
        Method (call me)
        params:
            user_info: INT32
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleNotifyUserInfoPrependSectionBreak(*arg, **kw)

    def PurpleNotifyUserInfoAddSectionHeader(self, *arg, **kw):
        '''
        Method (call me)
        params:
            user_info: INT32
            label: STRING
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleNotifyUserInfoAddSectionHeader(*arg, **kw)

    def PurpleNotifyUserInfoPrependSectionHeader(self, *arg, **kw):
        '''
        Method (call me)
        params:
            user_info: INT32
            label: STRING
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleNotifyUserInfoPrependSectionHeader(*arg, **kw)

    def PurpleNotifyUserInfoRemoveLastItem(self, *arg, **kw):
        '''
        Method (call me)
        params:
            user_info: INT32
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleNotifyUserInfoRemoveLastItem(*arg, **kw)

    def PurpleNotifyUserInfoEntryGetLabel(self, *arg, **kw):
        '''
        Method (call me)
        params:
            user_info_entry: INT32
            
        return:
            RESULT: STRING
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleNotifyUserInfoEntryGetLabel(*arg, **kw)

    def PurpleNotifyUserInfoEntrySetLabel(self, *arg, **kw):
        '''
        Method (call me)
        params:
            user_info_entry: INT32
            label: STRING
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleNotifyUserInfoEntrySetLabel(*arg, **kw)

    def PurpleNotifyUserInfoEntryGetValue(self, *arg, **kw):
        '''
        Method (call me)
        params:
            user_info_entry: INT32
            
        return:
            RESULT: STRING
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleNotifyUserInfoEntryGetValue(*arg, **kw)

    def PurpleNotifyUserInfoEntrySetValue(self, *arg, **kw):
        '''
        Method (call me)
        params:
            user_info_entry: INT32
            value: STRING
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleNotifyUserInfoEntrySetValue(*arg, **kw)

    def PurpleNotifyUserInfoEntryGetType(self, *arg, **kw):
        '''
        Method (call me)
        params:
            user_info_entry: INT32
            
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleNotifyUserInfoEntryGetType(*arg, **kw)

    def PurpleNotifyUserInfoEntrySetType(self, *arg, **kw):
        '''
        Method (call me)
        params:
            user_info_entry: INT32
            type: INT32
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleNotifyUserInfoEntrySetType(*arg, **kw)

    def PurpleNotifyClose(self, *arg, **kw):
        '''
        Method (call me)
        params:
            type: INT32
            ui_handle: INT32
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleNotifyClose(*arg, **kw)

    def PurpleNotifyCloseWithHandle(self, *arg, **kw):
        '''
        Method (call me)
        params:
            handle: INT32
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleNotifyCloseWithHandle(*arg, **kw)

    def PurpleNotifySetUiOps(self, *arg, **kw):
        '''
        Method (call me)
        params:
            ops: INT32
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleNotifySetUiOps(*arg, **kw)

    def PurpleNotifyGetUiOps(self, *arg, **kw):
        '''
        Method (call me)
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleNotifyGetUiOps(*arg, **kw)

    def PurpleNotifyInit(self, *arg, **kw):
        '''
        Method (call me)
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleNotifyInit(*arg, **kw)

    def PurpleNotifyUninit(self, *arg, **kw):
        '''
        Method (call me)
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleNotifyUninit(*arg, **kw)

    def PurplePrefsInit(self, *arg, **kw):
        '''
        Method (call me)
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurplePrefsInit(*arg, **kw)

    def PurplePrefsUninit(self, *arg, **kw):
        '''
        Method (call me)
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurplePrefsUninit(*arg, **kw)

    def PurplePrefsAddNone(self, *arg, **kw):
        '''
        Method (call me)
        params:
            name: STRING
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurplePrefsAddNone(*arg, **kw)

    def PurplePrefsAddBool(self, *arg, **kw):
        '''
        Method (call me)
        params:
            name: STRING
            value: INT32
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurplePrefsAddBool(*arg, **kw)

    def PurplePrefsAddInt(self, *arg, **kw):
        '''
        Method (call me)
        params:
            name: STRING
            value: INT32
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurplePrefsAddInt(*arg, **kw)

    def PurplePrefsAddString(self, *arg, **kw):
        '''
        Method (call me)
        params:
            name: STRING
            value: STRING
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurplePrefsAddString(*arg, **kw)

    def PurplePrefsAddStringList(self, *arg, **kw):
        '''
        Method (call me)
        params:
            name: STRING
            value: INT32
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurplePrefsAddStringList(*arg, **kw)

    def PurplePrefsAddPath(self, *arg, **kw):
        '''
        Method (call me)
        params:
            name: STRING
            value: STRING
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurplePrefsAddPath(*arg, **kw)

    def PurplePrefsAddPathList(self, *arg, **kw):
        '''
        Method (call me)
        params:
            name: STRING
            value: INT32
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurplePrefsAddPathList(*arg, **kw)

    def PurplePrefsRemove(self, *arg, **kw):
        '''
        Method (call me)
        params:
            name: STRING
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurplePrefsRemove(*arg, **kw)

    def PurplePrefsRename(self, *arg, **kw):
        '''
        Method (call me)
        params:
            oldname: STRING
            newname: STRING
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurplePrefsRename(*arg, **kw)

    def PurplePrefsRenameBooleanToggle(self, *arg, **kw):
        '''
        Method (call me)
        params:
            oldname: STRING
            newname: STRING
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurplePrefsRenameBooleanToggle(*arg, **kw)

    def PurplePrefsDestroy(self, *arg, **kw):
        '''
        Method (call me)
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurplePrefsDestroy(*arg, **kw)

    def PurplePrefsSetBool(self, *arg, **kw):
        '''
        Method (call me)
        params:
            name: STRING
            value: INT32
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurplePrefsSetBool(*arg, **kw)

    def PurplePrefsSetInt(self, *arg, **kw):
        '''
        Method (call me)
        params:
            name: STRING
            value: INT32
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurplePrefsSetInt(*arg, **kw)

    def PurplePrefsSetString(self, *arg, **kw):
        '''
        Method (call me)
        params:
            name: STRING
            value: STRING
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurplePrefsSetString(*arg, **kw)

    def PurplePrefsSetStringList(self, *arg, **kw):
        '''
        Method (call me)
        params:
            name: STRING
            value: INT32
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurplePrefsSetStringList(*arg, **kw)

    def PurplePrefsSetPath(self, *arg, **kw):
        '''
        Method (call me)
        params:
            name: STRING
            value: STRING
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurplePrefsSetPath(*arg, **kw)

    def PurplePrefsSetPathList(self, *arg, **kw):
        '''
        Method (call me)
        params:
            name: STRING
            value: INT32
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurplePrefsSetPathList(*arg, **kw)

    def PurplePrefsExists(self, *arg, **kw):
        '''
        Method (call me)
        params:
            name: STRING
            
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurplePrefsExists(*arg, **kw)

    def PurplePrefsGetType(self, *arg, **kw):
        '''
        Method (call me)
        params:
            name: STRING
            
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurplePrefsGetType(*arg, **kw)

    def PurplePrefsGetBool(self, *arg, **kw):
        '''
        Method (call me)
        params:
            name: STRING
            
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurplePrefsGetBool(*arg, **kw)

    def PurplePrefsGetInt(self, *arg, **kw):
        '''
        Method (call me)
        params:
            name: STRING
            
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurplePrefsGetInt(*arg, **kw)

    def PurplePrefsGetString(self, *arg, **kw):
        '''
        Method (call me)
        params:
            name: STRING
            
        return:
            RESULT: STRING
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurplePrefsGetString(*arg, **kw)

    def PurplePrefsGetStringList(self, *arg, **kw):
        '''
        Method (call me)
        params:
            name: STRING
            
        return:
            RESULT: as
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurplePrefsGetStringList(*arg, **kw)

    def PurplePrefsGetPath(self, *arg, **kw):
        '''
        Method (call me)
        params:
            name: STRING
            
        return:
            RESULT: STRING
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurplePrefsGetPath(*arg, **kw)

    def PurplePrefsGetPathList(self, *arg, **kw):
        '''
        Method (call me)
        params:
            name: STRING
            
        return:
            RESULT: as
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurplePrefsGetPathList(*arg, **kw)

    def PurplePrefsGetChildrenNames(self, *arg, **kw):
        '''
        Method (call me)
        params:
            name: STRING
            
        return:
            RESULT: as
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurplePrefsGetChildrenNames(*arg, **kw)

    def PurplePrefsDisconnectCallback(self, *arg, **kw):
        '''
        Method (call me)
        params:
            callback_id: INT32
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurplePrefsDisconnectCallback(*arg, **kw)

    def PurplePrefsDisconnectByHandle(self, *arg, **kw):
        '''
        Method (call me)
        params:
            handle: INT32
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurplePrefsDisconnectByHandle(*arg, **kw)

    def PurplePrefsTriggerCallback(self, *arg, **kw):
        '''
        Method (call me)
        params:
            name: STRING
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurplePrefsTriggerCallback(*arg, **kw)

    def PurplePrefsLoad(self, *arg, **kw):
        '''
        Method (call me)
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurplePrefsLoad(*arg, **kw)

    def PurplePrefsUpdateOld(self, *arg, **kw):
        '''
        Method (call me)
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurplePrefsUpdateOld(*arg, **kw)

    def PurpleRoomlistShowWithAccount(self, *arg, **kw):
        '''
        Method (call me)
        params:
            account: INT32
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleRoomlistShowWithAccount(*arg, **kw)

    def PurpleRoomlistNew(self, *arg, **kw):
        '''
        Method (call me)
        params:
            account: INT32
            
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleRoomlistNew(*arg, **kw)

    def PurpleRoomlistRef(self, *arg, **kw):
        '''
        Method (call me)
        params:
            list: INT32
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleRoomlistRef(*arg, **kw)

    def PurpleRoomlistUnref(self, *arg, **kw):
        '''
        Method (call me)
        params:
            list: INT32
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleRoomlistUnref(*arg, **kw)

    def PurpleRoomlistSetFields(self, *arg, **kw):
        '''
        Method (call me)
        params:
            list: INT32
            fields: INT32
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleRoomlistSetFields(*arg, **kw)

    def PurpleRoomlistSetInProgress(self, *arg, **kw):
        '''
        Method (call me)
        params:
            list: INT32
            in_progress: INT32
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleRoomlistSetInProgress(*arg, **kw)

    def PurpleRoomlistGetInProgress(self, *arg, **kw):
        '''
        Method (call me)
        params:
            list: INT32
            
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleRoomlistGetInProgress(*arg, **kw)

    def PurpleRoomlistRoomAdd(self, *arg, **kw):
        '''
        Method (call me)
        params:
            list: INT32
            room: INT32
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleRoomlistRoomAdd(*arg, **kw)

    def PurpleRoomlistGetList(self, *arg, **kw):
        '''
        Method (call me)
        params:
            gc: INT32
            
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleRoomlistGetList(*arg, **kw)

    def PurpleRoomlistCancelGetList(self, *arg, **kw):
        '''
        Method (call me)
        params:
            list: INT32
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleRoomlistCancelGetList(*arg, **kw)

    def PurpleRoomlistExpandCategory(self, *arg, **kw):
        '''
        Method (call me)
        params:
            list: INT32
            category: INT32
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleRoomlistExpandCategory(*arg, **kw)

    def PurpleRoomlistGetFields(self, *arg, **kw):
        '''
        Method (call me)
        params:
            roomlist: INT32
            
        return:
            RESULT: ai
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleRoomlistGetFields(*arg, **kw)

    def PurpleRoomlistRoomNew(self, *arg, **kw):
        '''
        Method (call me)
        params:
            type: INT32
            name: STRING
            parent: INT32
            
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleRoomlistRoomNew(*arg, **kw)

    def PurpleRoomlistRoomJoin(self, *arg, **kw):
        '''
        Method (call me)
        params:
            list: INT32
            room: INT32
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleRoomlistRoomJoin(*arg, **kw)

    def PurpleRoomlistRoomGetType(self, *arg, **kw):
        '''
        Method (call me)
        params:
            room: INT32
            
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleRoomlistRoomGetType(*arg, **kw)

    def PurpleRoomlistRoomGetName(self, *arg, **kw):
        '''
        Method (call me)
        params:
            room: INT32
            
        return:
            RESULT: STRING
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleRoomlistRoomGetName(*arg, **kw)

    def PurpleRoomlistRoomGetParent(self, *arg, **kw):
        '''
        Method (call me)
        params:
            room: INT32
            
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleRoomlistRoomGetParent(*arg, **kw)

    def PurpleRoomlistRoomGetFields(self, *arg, **kw):
        '''
        Method (call me)
        params:
            room: INT32
            
        return:
            RESULT: ai
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleRoomlistRoomGetFields(*arg, **kw)

    def PurpleRoomlistFieldNew(self, *arg, **kw):
        '''
        Method (call me)
        params:
            type: INT32
            label: STRING
            name: STRING
            hidden: INT32
            
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleRoomlistFieldNew(*arg, **kw)

    def PurpleRoomlistFieldGetType(self, *arg, **kw):
        '''
        Method (call me)
        params:
            field: INT32
            
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleRoomlistFieldGetType(*arg, **kw)

    def PurpleRoomlistFieldGetLabel(self, *arg, **kw):
        '''
        Method (call me)
        params:
            field: INT32
            
        return:
            RESULT: STRING
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleRoomlistFieldGetLabel(*arg, **kw)

    def PurpleRoomlistFieldGetHidden(self, *arg, **kw):
        '''
        Method (call me)
        params:
            field: INT32
            
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleRoomlistFieldGetHidden(*arg, **kw)

    def PurpleRoomlistSetUiOps(self, *arg, **kw):
        '''
        Method (call me)
        params:
            ops: INT32
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleRoomlistSetUiOps(*arg, **kw)

    def PurpleRoomlistGetUiOps(self, *arg, **kw):
        '''
        Method (call me)
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleRoomlistGetUiOps(*arg, **kw)

    def PurpleSavedstatusNew(self, *arg, **kw):
        '''
        Method (call me)
        params:
            title: STRING
            type: INT32
            
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleSavedstatusNew(*arg, **kw)

    def PurpleSavedstatusSetTitle(self, *arg, **kw):
        '''
        Method (call me)
        params:
            status: INT32
            title: STRING
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleSavedstatusSetTitle(*arg, **kw)

    def PurpleSavedstatusSetType(self, *arg, **kw):
        '''
        Method (call me)
        params:
            status: INT32
            type: INT32
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleSavedstatusSetType(*arg, **kw)

    def PurpleSavedstatusSetMessage(self, *arg, **kw):
        '''
        Method (call me)
        params:
            status: INT32
            message: STRING
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleSavedstatusSetMessage(*arg, **kw)

    def PurpleSavedstatusSetSubstatus(self, *arg, **kw):
        '''
        Method (call me)
        params:
            status: INT32
            account: INT32
            type: INT32
            message: STRING
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleSavedstatusSetSubstatus(*arg, **kw)

    def PurpleSavedstatusUnsetSubstatus(self, *arg, **kw):
        '''
        Method (call me)
        params:
            saved_status: INT32
            account: INT32
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleSavedstatusUnsetSubstatus(*arg, **kw)

    def PurpleSavedstatusDelete(self, *arg, **kw):
        '''
        Method (call me)
        params:
            title: STRING
            
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleSavedstatusDelete(*arg, **kw)

    def PurpleSavedstatusDeleteByStatus(self, *arg, **kw):
        '''
        Method (call me)
        params:
            saved_status: INT32
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleSavedstatusDeleteByStatus(*arg, **kw)

    def PurpleSavedstatusesGetAll(self, *arg, **kw):
        '''
        Method (call me)
        return:
            RESULT: ai
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleSavedstatusesGetAll(*arg, **kw)

    def PurpleSavedstatusesGetPopular(self, *arg, **kw):
        '''
        Method (call me)
        params:
            how_many: UINT32
            
        return:
            RESULT: ai
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleSavedstatusesGetPopular(*arg, **kw)

    def PurpleSavedstatusGetCurrent(self, *arg, **kw):
        '''
        Method (call me)
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleSavedstatusGetCurrent(*arg, **kw)

    def PurpleSavedstatusGetDefault(self, *arg, **kw):
        '''
        Method (call me)
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleSavedstatusGetDefault(*arg, **kw)

    def PurpleSavedstatusGetIdleaway(self, *arg, **kw):
        '''
        Method (call me)
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleSavedstatusGetIdleaway(*arg, **kw)

    def PurpleSavedstatusIsIdleaway(self, *arg, **kw):
        '''
        Method (call me)
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleSavedstatusIsIdleaway(*arg, **kw)

    def PurpleSavedstatusSetIdleaway(self, *arg, **kw):
        '''
        Method (call me)
        params:
            idleaway: INT32
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleSavedstatusSetIdleaway(*arg, **kw)

    def PurpleSavedstatusGetStartup(self, *arg, **kw):
        '''
        Method (call me)
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleSavedstatusGetStartup(*arg, **kw)

    def PurpleSavedstatusFind(self, *arg, **kw):
        '''
        Method (call me)
        params:
            title: STRING
            
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleSavedstatusFind(*arg, **kw)

    def PurpleSavedstatusFindByCreationTime(self, *arg, **kw):
        '''
        Method (call me)
        params:
            creation_time: INT32
            
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleSavedstatusFindByCreationTime(*arg, **kw)

    def PurpleSavedstatusFindTransientByTypeAndMessage(self, *arg, **kw):
        '''
        Method (call me)
        params:
            type: INT32
            message: STRING
            
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleSavedstatusFindTransientByTypeAndMessage(*arg, **kw)

    def PurpleSavedstatusIsTransient(self, *arg, **kw):
        '''
        Method (call me)
        params:
            saved_status: INT32
            
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleSavedstatusIsTransient(*arg, **kw)

    def PurpleSavedstatusGetTitle(self, *arg, **kw):
        '''
        Method (call me)
        params:
            saved_status: INT32
            
        return:
            RESULT: STRING
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleSavedstatusGetTitle(*arg, **kw)

    def PurpleSavedstatusGetType(self, *arg, **kw):
        '''
        Method (call me)
        params:
            saved_status: INT32
            
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleSavedstatusGetType(*arg, **kw)

    def PurpleSavedstatusGetMessage(self, *arg, **kw):
        '''
        Method (call me)
        params:
            saved_status: INT32
            
        return:
            RESULT: STRING
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleSavedstatusGetMessage(*arg, **kw)

    def PurpleSavedstatusGetCreationTime(self, *arg, **kw):
        '''
        Method (call me)
        params:
            saved_status: INT32
            
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleSavedstatusGetCreationTime(*arg, **kw)

    def PurpleSavedstatusHasSubstatuses(self, *arg, **kw):
        '''
        Method (call me)
        params:
            saved_status: INT32
            
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleSavedstatusHasSubstatuses(*arg, **kw)

    def PurpleSavedstatusGetSubstatus(self, *arg, **kw):
        '''
        Method (call me)
        params:
            saved_status: INT32
            account: INT32
            
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleSavedstatusGetSubstatus(*arg, **kw)

    def PurpleSavedstatusSubstatusGetType(self, *arg, **kw):
        '''
        Method (call me)
        params:
            substatus: INT32
            
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleSavedstatusSubstatusGetType(*arg, **kw)

    def PurpleSavedstatusSubstatusGetMessage(self, *arg, **kw):
        '''
        Method (call me)
        params:
            substatus: INT32
            
        return:
            RESULT: STRING
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleSavedstatusSubstatusGetMessage(*arg, **kw)

    def PurpleSavedstatusActivate(self, *arg, **kw):
        '''
        Method (call me)
        params:
            saved_status: INT32
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleSavedstatusActivate(*arg, **kw)

    def PurpleSavedstatusActivateForAccount(self, *arg, **kw):
        '''
        Method (call me)
        params:
            saved_status: INT32
            account: INT32
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleSavedstatusActivateForAccount(*arg, **kw)

    def PurpleSavedstatusesInit(self, *arg, **kw):
        '''
        Method (call me)
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleSavedstatusesInit(*arg, **kw)

    def PurpleSavedstatusesUninit(self, *arg, **kw):
        '''
        Method (call me)
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleSavedstatusesUninit(*arg, **kw)

    def PurpleSmileyNew(self, *arg, **kw):
        '''
        Method (call me)
        params:
            img: INT32
            shortcut: STRING
            
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleSmileyNew(*arg, **kw)

    def PurpleSmileyNewFromFile(self, *arg, **kw):
        '''
        Method (call me)
        params:
            shortcut: STRING
            filepath: STRING
            
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleSmileyNewFromFile(*arg, **kw)

    def PurpleSmileyDelete(self, *arg, **kw):
        '''
        Method (call me)
        params:
            smiley: INT32
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleSmileyDelete(*arg, **kw)

    def PurpleSmileySetShortcut(self, *arg, **kw):
        '''
        Method (call me)
        params:
            smiley: INT32
            shortcut: STRING
            
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleSmileySetShortcut(*arg, **kw)

    def PurpleSmileySetData(self, *arg, **kw):
        '''
        Method (call me)
        params:
            smiley: INT32
            smiley_data: INT32
            smiley_data_len: INT32
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleSmileySetData(*arg, **kw)

    def PurpleSmileyGetShortcut(self, *arg, **kw):
        '''
        Method (call me)
        params:
            smiley: INT32
            
        return:
            RESULT: STRING
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleSmileyGetShortcut(*arg, **kw)

    def PurpleSmileyGetChecksum(self, *arg, **kw):
        '''
        Method (call me)
        params:
            smiley: INT32
            
        return:
            RESULT: STRING
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleSmileyGetChecksum(*arg, **kw)

    def PurpleSmileyGetStoredImage(self, *arg, **kw):
        '''
        Method (call me)
        params:
            smiley: INT32
            
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleSmileyGetStoredImage(*arg, **kw)

    def PurpleSmileyGetData(self, *arg, **kw):
        '''
        Method (call me)
        params:
            smiley: INT32
            
        return:
            RESULT: ay
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleSmileyGetData(*arg, **kw)

    def PurpleSmileyGetExtension(self, *arg, **kw):
        '''
        Method (call me)
        params:
            smiley: INT32
            
        return:
            RESULT: STRING
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleSmileyGetExtension(*arg, **kw)

    def PurpleSmileyGetFullPath(self, *arg, **kw):
        '''
        Method (call me)
        params:
            smiley: INT32
            
        return:
            RESULT: STRING
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleSmileyGetFullPath(*arg, **kw)

    def PurpleSmileysGetAll(self, *arg, **kw):
        '''
        Method (call me)
        return:
            RESULT: ai
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleSmileysGetAll(*arg, **kw)

    def PurpleSmileysFindByShortcut(self, *arg, **kw):
        '''
        Method (call me)
        params:
            shortcut: STRING
            
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleSmileysFindByShortcut(*arg, **kw)

    def PurpleSmileysFindByChecksum(self, *arg, **kw):
        '''
        Method (call me)
        params:
            checksum: STRING
            
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleSmileysFindByChecksum(*arg, **kw)

    def PurpleSmileysGetStoringDir(self, *arg, **kw):
        '''
        Method (call me)
        return:
            RESULT: STRING
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleSmileysGetStoringDir(*arg, **kw)

    def PurpleSmileysInit(self, *arg, **kw):
        '''
        Method (call me)
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleSmileysInit(*arg, **kw)

    def PurpleSmileysUninit(self, *arg, **kw):
        '''
        Method (call me)
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleSmileysUninit(*arg, **kw)

    def PurplePrimitiveGetIdFromType(self, *arg, **kw):
        '''
        Method (call me)
        params:
            type: INT32
            
        return:
            RESULT: STRING
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurplePrimitiveGetIdFromType(*arg, **kw)

    def PurplePrimitiveGetNameFromType(self, *arg, **kw):
        '''
        Method (call me)
        params:
            type: INT32
            
        return:
            RESULT: STRING
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurplePrimitiveGetNameFromType(*arg, **kw)

    def PurplePrimitiveGetTypeFromId(self, *arg, **kw):
        '''
        Method (call me)
        params:
            id: STRING
            
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurplePrimitiveGetTypeFromId(*arg, **kw)

    def PurpleStatusTypeNewFull(self, *arg, **kw):
        '''
        Method (call me)
        params:
            primitive: INT32
            id: STRING
            name: STRING
            saveable: INT32
            user_settable: INT32
            independent: INT32
            
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleStatusTypeNewFull(*arg, **kw)

    def PurpleStatusTypeNew(self, *arg, **kw):
        '''
        Method (call me)
        params:
            primitive: INT32
            id: STRING
            name: STRING
            user_settable: INT32
            
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleStatusTypeNew(*arg, **kw)

    def PurpleStatusTypeDestroy(self, *arg, **kw):
        '''
        Method (call me)
        params:
            status_type: INT32
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleStatusTypeDestroy(*arg, **kw)

    def PurpleStatusTypeSetPrimaryAttr(self, *arg, **kw):
        '''
        Method (call me)
        params:
            status_type: INT32
            attr_id: STRING
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleStatusTypeSetPrimaryAttr(*arg, **kw)

    def PurpleStatusTypeAddAttr(self, *arg, **kw):
        '''
        Method (call me)
        params:
            status_type: INT32
            id: STRING
            name: STRING
            value: INT32
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleStatusTypeAddAttr(*arg, **kw)

    def PurpleStatusTypeGetPrimitive(self, *arg, **kw):
        '''
        Method (call me)
        params:
            status_type: INT32
            
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleStatusTypeGetPrimitive(*arg, **kw)

    def PurpleStatusTypeGetId(self, *arg, **kw):
        '''
        Method (call me)
        params:
            status_type: INT32
            
        return:
            RESULT: STRING
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleStatusTypeGetId(*arg, **kw)

    def PurpleStatusTypeGetName(self, *arg, **kw):
        '''
        Method (call me)
        params:
            status_type: INT32
            
        return:
            RESULT: STRING
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleStatusTypeGetName(*arg, **kw)

    def PurpleStatusTypeIsSaveable(self, *arg, **kw):
        '''
        Method (call me)
        params:
            status_type: INT32
            
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleStatusTypeIsSaveable(*arg, **kw)

    def PurpleStatusTypeIsUserSettable(self, *arg, **kw):
        '''
        Method (call me)
        params:
            status_type: INT32
            
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleStatusTypeIsUserSettable(*arg, **kw)

    def PurpleStatusTypeIsIndependent(self, *arg, **kw):
        '''
        Method (call me)
        params:
            status_type: INT32
            
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleStatusTypeIsIndependent(*arg, **kw)

    def PurpleStatusTypeIsExclusive(self, *arg, **kw):
        '''
        Method (call me)
        params:
            status_type: INT32
            
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleStatusTypeIsExclusive(*arg, **kw)

    def PurpleStatusTypeIsAvailable(self, *arg, **kw):
        '''
        Method (call me)
        params:
            status_type: INT32
            
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleStatusTypeIsAvailable(*arg, **kw)

    def PurpleStatusTypeGetPrimaryAttr(self, *arg, **kw):
        '''
        Method (call me)
        params:
            type: INT32
            
        return:
            RESULT: STRING
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleStatusTypeGetPrimaryAttr(*arg, **kw)

    def PurpleStatusTypeGetAttr(self, *arg, **kw):
        '''
        Method (call me)
        params:
            status_type: INT32
            id: STRING
            
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleStatusTypeGetAttr(*arg, **kw)

    def PurpleStatusTypeGetAttrs(self, *arg, **kw):
        '''
        Method (call me)
        params:
            status_type: INT32
            
        return:
            RESULT: ai
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleStatusTypeGetAttrs(*arg, **kw)

    def PurpleStatusTypeFindWithId(self, *arg, **kw):
        '''
        Method (call me)
        params:
            status_types: INT32
            id: STRING
            
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleStatusTypeFindWithId(*arg, **kw)

    def PurpleStatusAttrNew(self, *arg, **kw):
        '''
        Method (call me)
        params:
            id: STRING
            name: STRING
            value_type: INT32
            
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleStatusAttrNew(*arg, **kw)

    def PurpleStatusAttrDestroy(self, *arg, **kw):
        '''
        Method (call me)
        params:
            attr: INT32
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleStatusAttrDestroy(*arg, **kw)

    def PurpleStatusAttrGetId(self, *arg, **kw):
        '''
        Method (call me)
        params:
            attr: INT32
            
        return:
            RESULT: STRING
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleStatusAttrGetId(*arg, **kw)

    def PurpleStatusAttrGetName(self, *arg, **kw):
        '''
        Method (call me)
        params:
            attr: INT32
            
        return:
            RESULT: STRING
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleStatusAttrGetName(*arg, **kw)

    def PurpleStatusAttrGetValue(self, *arg, **kw):
        '''
        Method (call me)
        params:
            attr: INT32
            
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleStatusAttrGetValue(*arg, **kw)

    def PurpleStatusNew(self, *arg, **kw):
        '''
        Method (call me)
        params:
            status_type: INT32
            presence: INT32
            
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleStatusNew(*arg, **kw)

    def PurpleStatusDestroy(self, *arg, **kw):
        '''
        Method (call me)
        params:
            status: INT32
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleStatusDestroy(*arg, **kw)

    def PurpleStatusSetActive(self, *arg, **kw):
        '''
        Method (call me)
        params:
            status: INT32
            active: INT32
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleStatusSetActive(*arg, **kw)

    def PurpleStatusSetActiveWithAttrsList(self, *arg, **kw):
        '''
        Method (call me)
        params:
            status: INT32
            active: INT32
            attrs: INT32
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleStatusSetActiveWithAttrsList(*arg, **kw)

    def PurpleStatusSetAttrBoolean(self, *arg, **kw):
        '''
        Method (call me)
        params:
            status: INT32
            id: STRING
            value: INT32
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleStatusSetAttrBoolean(*arg, **kw)

    def PurpleStatusSetAttrInt(self, *arg, **kw):
        '''
        Method (call me)
        params:
            status: INT32
            id: STRING
            value: INT32
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleStatusSetAttrInt(*arg, **kw)

    def PurpleStatusSetAttrString(self, *arg, **kw):
        '''
        Method (call me)
        params:
            status: INT32
            id: STRING
            value: STRING
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleStatusSetAttrString(*arg, **kw)

    def PurpleStatusGetType(self, *arg, **kw):
        '''
        Method (call me)
        params:
            status: INT32
            
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleStatusGetType(*arg, **kw)

    def PurpleStatusGetPresence(self, *arg, **kw):
        '''
        Method (call me)
        params:
            status: INT32
            
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleStatusGetPresence(*arg, **kw)

    def PurpleStatusGetId(self, *arg, **kw):
        '''
        Method (call me)
        params:
            status: INT32
            
        return:
            RESULT: STRING
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleStatusGetId(*arg, **kw)

    def PurpleStatusGetName(self, *arg, **kw):
        '''
        Method (call me)
        params:
            status: INT32
            
        return:
            RESULT: STRING
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleStatusGetName(*arg, **kw)

    def PurpleStatusIsIndependent(self, *arg, **kw):
        '''
        Method (call me)
        params:
            status: INT32
            
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleStatusIsIndependent(*arg, **kw)

    def PurpleStatusIsExclusive(self, *arg, **kw):
        '''
        Method (call me)
        params:
            status: INT32
            
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleStatusIsExclusive(*arg, **kw)

    def PurpleStatusIsAvailable(self, *arg, **kw):
        '''
        Method (call me)
        params:
            status: INT32
            
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleStatusIsAvailable(*arg, **kw)

    def PurpleStatusIsActive(self, *arg, **kw):
        '''
        Method (call me)
        params:
            status: INT32
            
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleStatusIsActive(*arg, **kw)

    def PurpleStatusIsOnline(self, *arg, **kw):
        '''
        Method (call me)
        params:
            status: INT32
            
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleStatusIsOnline(*arg, **kw)

    def PurpleStatusGetAttrValue(self, *arg, **kw):
        '''
        Method (call me)
        params:
            status: INT32
            id: STRING
            
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleStatusGetAttrValue(*arg, **kw)

    def PurpleStatusGetAttrBoolean(self, *arg, **kw):
        '''
        Method (call me)
        params:
            status: INT32
            id: STRING
            
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleStatusGetAttrBoolean(*arg, **kw)

    def PurpleStatusGetAttrInt(self, *arg, **kw):
        '''
        Method (call me)
        params:
            status: INT32
            id: STRING
            
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleStatusGetAttrInt(*arg, **kw)

    def PurpleStatusGetAttrString(self, *arg, **kw):
        '''
        Method (call me)
        params:
            status: INT32
            id: STRING
            
        return:
            RESULT: STRING
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleStatusGetAttrString(*arg, **kw)

    def PurpleStatusCompare(self, *arg, **kw):
        '''
        Method (call me)
        params:
            status1: INT32
            status2: INT32
            
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleStatusCompare(*arg, **kw)

    def PurplePresenceNew(self, *arg, **kw):
        '''
        Method (call me)
        params:
            context: INT32
            
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurplePresenceNew(*arg, **kw)

    def PurplePresenceNewForAccount(self, *arg, **kw):
        '''
        Method (call me)
        params:
            account: INT32
            
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurplePresenceNewForAccount(*arg, **kw)

    def PurplePresenceNewForConv(self, *arg, **kw):
        '''
        Method (call me)
        params:
            conv: INT32
            
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurplePresenceNewForConv(*arg, **kw)

    def PurplePresenceNewForBuddy(self, *arg, **kw):
        '''
        Method (call me)
        params:
            buddy: INT32
            
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurplePresenceNewForBuddy(*arg, **kw)

    def PurplePresenceDestroy(self, *arg, **kw):
        '''
        Method (call me)
        params:
            presence: INT32
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurplePresenceDestroy(*arg, **kw)

    def PurplePresenceAddStatus(self, *arg, **kw):
        '''
        Method (call me)
        params:
            presence: INT32
            status: INT32
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurplePresenceAddStatus(*arg, **kw)

    def PurplePresenceSetStatusActive(self, *arg, **kw):
        '''
        Method (call me)
        params:
            presence: INT32
            status_id: STRING
            active: INT32
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurplePresenceSetStatusActive(*arg, **kw)

    def PurplePresenceSwitchStatus(self, *arg, **kw):
        '''
        Method (call me)
        params:
            presence: INT32
            status_id: STRING
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurplePresenceSwitchStatus(*arg, **kw)

    def PurplePresenceSetIdle(self, *arg, **kw):
        '''
        Method (call me)
        params:
            presence: INT32
            idle: INT32
            idle_time: INT32
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurplePresenceSetIdle(*arg, **kw)

    def PurplePresenceSetLoginTime(self, *arg, **kw):
        '''
        Method (call me)
        params:
            presence: INT32
            login_time: INT32
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurplePresenceSetLoginTime(*arg, **kw)

    def PurplePresenceGetContext(self, *arg, **kw):
        '''
        Method (call me)
        params:
            presence: INT32
            
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurplePresenceGetContext(*arg, **kw)

    def PurplePresenceGetAccount(self, *arg, **kw):
        '''
        Method (call me)
        params:
            presence: INT32
            
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurplePresenceGetAccount(*arg, **kw)

    def PurplePresenceGetConversation(self, *arg, **kw):
        '''
        Method (call me)
        params:
            presence: INT32
            
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurplePresenceGetConversation(*arg, **kw)

    def PurplePresenceGetChatUser(self, *arg, **kw):
        '''
        Method (call me)
        params:
            presence: INT32
            
        return:
            RESULT: STRING
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurplePresenceGetChatUser(*arg, **kw)

    def PurplePresenceGetBuddy(self, *arg, **kw):
        '''
        Method (call me)
        params:
            presence: INT32
            
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurplePresenceGetBuddy(*arg, **kw)

    def PurplePresenceGetStatuses(self, *arg, **kw):
        '''
        Method (call me)
        params:
            presence: INT32
            
        return:
            RESULT: ai
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurplePresenceGetStatuses(*arg, **kw)

    def PurplePresenceGetStatus(self, *arg, **kw):
        '''
        Method (call me)
        params:
            presence: INT32
            status_id: STRING
            
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurplePresenceGetStatus(*arg, **kw)

    def PurplePresenceGetActiveStatus(self, *arg, **kw):
        '''
        Method (call me)
        params:
            presence: INT32
            
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurplePresenceGetActiveStatus(*arg, **kw)

    def PurplePresenceIsAvailable(self, *arg, **kw):
        '''
        Method (call me)
        params:
            presence: INT32
            
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurplePresenceIsAvailable(*arg, **kw)

    def PurplePresenceIsOnline(self, *arg, **kw):
        '''
        Method (call me)
        params:
            presence: INT32
            
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurplePresenceIsOnline(*arg, **kw)

    def PurplePresenceIsStatusActive(self, *arg, **kw):
        '''
        Method (call me)
        params:
            presence: INT32
            status_id: STRING
            
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurplePresenceIsStatusActive(*arg, **kw)

    def PurplePresenceIsStatusPrimitiveActive(self, *arg, **kw):
        '''
        Method (call me)
        params:
            presence: INT32
            primitive: INT32
            
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurplePresenceIsStatusPrimitiveActive(*arg, **kw)

    def PurplePresenceIsIdle(self, *arg, **kw):
        '''
        Method (call me)
        params:
            presence: INT32
            
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurplePresenceIsIdle(*arg, **kw)

    def PurplePresenceGetIdleTime(self, *arg, **kw):
        '''
        Method (call me)
        params:
            presence: INT32
            
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurplePresenceGetIdleTime(*arg, **kw)

    def PurplePresenceGetLoginTime(self, *arg, **kw):
        '''
        Method (call me)
        params:
            presence: INT32
            
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurplePresenceGetLoginTime(*arg, **kw)

    def PurplePresenceCompare(self, *arg, **kw):
        '''
        Method (call me)
        params:
            presence1: INT32
            presence2: INT32
            
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurplePresenceCompare(*arg, **kw)

    def PurpleStatusInit(self, *arg, **kw):
        '''
        Method (call me)
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleStatusInit(*arg, **kw)

    def PurpleStatusUninit(self, *arg, **kw):
        '''
        Method (call me)
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleStatusUninit(*arg, **kw)

    def ServSendTyping(self, *arg, **kw):
        '''
        Method (call me)
        params:
            gc: INT32
            name: STRING
            state: INT32
            
        return:
            RESULT: UINT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.ServSendTyping(*arg, **kw)

    def ServMoveBuddy(self, *arg, **kw):
        '''
        Method (call me)
        params:
            param0: INT32
            param1: INT32
            param2: INT32
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.ServMoveBuddy(*arg, **kw)

    def ServSendIm(self, *arg, **kw):
        '''
        Method (call me)
        params:
            param0: INT32
            param1: STRING
            param2: STRING
            flags: INT32
            
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.ServSendIm(*arg, **kw)

    def PurpleGetAttentionTypeFromCode(self, *arg, **kw):
        '''
        Method (call me)
        params:
            account: INT32
            type_code: INT32
            
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleGetAttentionTypeFromCode(*arg, **kw)

    def ServSendAttention(self, *arg, **kw):
        '''
        Method (call me)
        params:
            gc: INT32
            who: STRING
            type_code: INT32
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.ServSendAttention(*arg, **kw)

    def ServGotAttention(self, *arg, **kw):
        '''
        Method (call me)
        params:
            gc: INT32
            who: STRING
            type_code: INT32
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.ServGotAttention(*arg, **kw)

    def ServGetInfo(self, *arg, **kw):
        '''
        Method (call me)
        params:
            param0: INT32
            param1: STRING
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.ServGetInfo(*arg, **kw)

    def ServSetInfo(self, *arg, **kw):
        '''
        Method (call me)
        params:
            param0: INT32
            param1: STRING
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.ServSetInfo(*arg, **kw)

    def ServAddPermit(self, *arg, **kw):
        '''
        Method (call me)
        params:
            param0: INT32
            param1: STRING
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.ServAddPermit(*arg, **kw)

    def ServAddDeny(self, *arg, **kw):
        '''
        Method (call me)
        params:
            param0: INT32
            param1: STRING
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.ServAddDeny(*arg, **kw)

    def ServRemPermit(self, *arg, **kw):
        '''
        Method (call me)
        params:
            param0: INT32
            param1: STRING
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.ServRemPermit(*arg, **kw)

    def ServRemDeny(self, *arg, **kw):
        '''
        Method (call me)
        params:
            param0: INT32
            param1: STRING
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.ServRemDeny(*arg, **kw)

    def ServSetPermitDeny(self, *arg, **kw):
        '''
        Method (call me)
        params:
            param0: INT32
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.ServSetPermitDeny(*arg, **kw)

    def ServChatInvite(self, *arg, **kw):
        '''
        Method (call me)
        params:
            param0: INT32
            param1: INT32
            param2: STRING
            param3: STRING
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.ServChatInvite(*arg, **kw)

    def ServChatLeave(self, *arg, **kw):
        '''
        Method (call me)
        params:
            param0: INT32
            param1: INT32
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.ServChatLeave(*arg, **kw)

    def ServChatWhisper(self, *arg, **kw):
        '''
        Method (call me)
        params:
            param0: INT32
            param1: INT32
            param2: STRING
            param3: STRING
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.ServChatWhisper(*arg, **kw)

    def ServChatSend(self, *arg, **kw):
        '''
        Method (call me)
        params:
            param0: INT32
            param1: INT32
            param2: STRING
            flags: INT32
            
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.ServChatSend(*arg, **kw)

    def ServAliasBuddy(self, *arg, **kw):
        '''
        Method (call me)
        params:
            param0: INT32
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.ServAliasBuddy(*arg, **kw)

    def ServGotAlias(self, *arg, **kw):
        '''
        Method (call me)
        params:
            gc: INT32
            who: STRING
            alias: STRING
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.ServGotAlias(*arg, **kw)

    def PurpleServGotPrivateAlias(self, *arg, **kw):
        '''
        Method (call me)
        params:
            gc: INT32
            who: STRING
            alias: STRING
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleServGotPrivateAlias(*arg, **kw)

    def ServGotTyping(self, *arg, **kw):
        '''
        Method (call me)
        params:
            gc: INT32
            name: STRING
            timeout: INT32
            state: INT32
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.ServGotTyping(*arg, **kw)

    def ServGotTypingStopped(self, *arg, **kw):
        '''
        Method (call me)
        params:
            gc: INT32
            name: STRING
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.ServGotTypingStopped(*arg, **kw)

    def ServGotIm(self, *arg, **kw):
        '''
        Method (call me)
        params:
            gc: INT32
            who: STRING
            msg: STRING
            flags: INT32
            mtime: INT32
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.ServGotIm(*arg, **kw)

    def ServJoinChat(self, *arg, **kw):
        '''
        Method (call me)
        params:
            param0: INT32
            data: a{ss}
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.ServJoinChat(*arg, **kw)

    def ServRejectChat(self, *arg, **kw):
        '''
        Method (call me)
        params:
            param0: INT32
            data: a{ss}
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.ServRejectChat(*arg, **kw)

    def ServGotChatInvite(self, *arg, **kw):
        '''
        Method (call me)
        params:
            gc: INT32
            name: STRING
            who: STRING
            message: STRING
            data: a{ss}
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.ServGotChatInvite(*arg, **kw)

    def ServGotJoinedChat(self, *arg, **kw):
        '''
        Method (call me)
        params:
            gc: INT32
            id: INT32
            name: STRING
            
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.ServGotJoinedChat(*arg, **kw)

    def PurpleServGotJoinChatFailed(self, *arg, **kw):
        '''
        Method (call me)
        params:
            gc: INT32
            data: a{ss}
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleServGotJoinChatFailed(*arg, **kw)

    def ServGotChatLeft(self, *arg, **kw):
        '''
        Method (call me)
        params:
            g: INT32
            id: INT32
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.ServGotChatLeft(*arg, **kw)

    def ServGotChatIn(self, *arg, **kw):
        '''
        Method (call me)
        params:
            g: INT32
            id: INT32
            who: STRING
            flags: INT32
            message: STRING
            mtime: INT32
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.ServGotChatIn(*arg, **kw)

    def ServSendFile(self, *arg, **kw):
        '''
        Method (call me)
        params:
            gc: INT32
            who: STRING
            file: STRING
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.ServSendFile(*arg, **kw)

    def PurpleMenuActionFree(self, *arg, **kw):
        '''
        Method (call me)
        params:
            act: INT32
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleMenuActionFree(*arg, **kw)

    def PurpleUtilSetCurrentSong(self, *arg, **kw):
        '''
        Method (call me)
        params:
            title: STRING
            artist: STRING
            album: STRING
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleUtilSetCurrentSong(*arg, **kw)

    def PurpleUtilInit(self, *arg, **kw):
        '''
        Method (call me)
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleUtilInit(*arg, **kw)

    def PurpleUtilUninit(self, *arg, **kw):
        '''
        Method (call me)
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleUtilUninit(*arg, **kw)

    def PurpleMimeDecodeField(self, *arg, **kw):
        '''
        Method (call me)
        params:
            str: STRING
            
        return:
            RESULT: STRING
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleMimeDecodeField(*arg, **kw)

    def PurpleTimeBuild(self, *arg, **kw):
        '''
        Method (call me)
        params:
            year: INT32
            month: INT32
            day: INT32
            hour: INT32
            min: INT32
            sec: INT32
            
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleTimeBuild(*arg, **kw)

    def PurpleMarkupEscapeText(self, *arg, **kw):
        '''
        Method (call me)
        params:
            text: STRING
            length: INT32
            
        return:
            RESULT: STRING
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleMarkupEscapeText(*arg, **kw)

    def PurpleMarkupStripHtml(self, *arg, **kw):
        '''
        Method (call me)
        params:
            str: STRING
            
        return:
            RESULT: STRING
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleMarkupStripHtml(*arg, **kw)

    def PurpleMarkupLinkify(self, *arg, **kw):
        '''
        Method (call me)
        params:
            str: STRING
            
        return:
            RESULT: STRING
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleMarkupLinkify(*arg, **kw)

    def PurpleUnescapeText(self, *arg, **kw):
        '''
        Method (call me)
        params:
            text: STRING
            
        return:
            RESULT: STRING
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleUnescapeText(*arg, **kw)

    def PurpleUnescapeHtml(self, *arg, **kw):
        '''
        Method (call me)
        params:
            html: STRING
            
        return:
            RESULT: STRING
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleUnescapeHtml(*arg, **kw)

    def PurpleMarkupSlice(self, *arg, **kw):
        '''
        Method (call me)
        params:
            str: STRING
            x: INT32
            y: INT32
            
        return:
            RESULT: STRING
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleMarkupSlice(*arg, **kw)

    def PurpleMarkupGetTagName(self, *arg, **kw):
        '''
        Method (call me)
        params:
            tag: STRING
            
        return:
            RESULT: STRING
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleMarkupGetTagName(*arg, **kw)

    def PurpleMarkupUnescapeEntity(self, *arg, **kw):
        '''
        Method (call me)
        params:
            text: STRING
            length: INT32
            
        return:
            RESULT: STRING
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleMarkupUnescapeEntity(*arg, **kw)

    def PurpleMarkupGetCssProperty(self, *arg, **kw):
        '''
        Method (call me)
        params:
            style: STRING
            opt: STRING
            
        return:
            RESULT: STRING
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleMarkupGetCssProperty(*arg, **kw)

    def PurpleMarkupIsRtl(self, *arg, **kw):
        '''
        Method (call me)
        params:
            html: STRING
            
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleMarkupIsRtl(*arg, **kw)

    def PurpleHomeDir(self, *arg, **kw):
        '''
        Method (call me)
        return:
            RESULT: STRING
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleHomeDir(*arg, **kw)

    def PurpleUserDir(self, *arg, **kw):
        '''
        Method (call me)
        return:
            RESULT: STRING
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleUserDir(*arg, **kw)

    def PurpleUtilSetUserDir(self, *arg, **kw):
        '''
        Method (call me)
        params:
            dir: STRING
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleUtilSetUserDir(*arg, **kw)

    def PurpleBuildDir(self, *arg, **kw):
        '''
        Method (call me)
        params:
            path: STRING
            mode: INT32
            
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleBuildDir(*arg, **kw)

    def PurpleUtilWriteDataToFile(self, *arg, **kw):
        '''
        Method (call me)
        params:
            filename: STRING
            data: STRING
            size: INT32
            
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleUtilWriteDataToFile(*arg, **kw)

    def PurpleUtilWriteDataToFileAbsolute(self, *arg, **kw):
        '''
        Method (call me)
        params:
            filename_full: STRING
            data: STRING
            size: INT32
            
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleUtilWriteDataToFileAbsolute(*arg, **kw)

    def PurpleProgramIsValid(self, *arg, **kw):
        '''
        Method (call me)
        params:
            program: STRING
            
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleProgramIsValid(*arg, **kw)

    def PurpleRunningGnome(self, *arg, **kw):
        '''
        Method (call me)
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleRunningGnome(*arg, **kw)

    def PurpleRunningKde(self, *arg, **kw):
        '''
        Method (call me)
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleRunningKde(*arg, **kw)

    def PurpleRunningOsx(self, *arg, **kw):
        '''
        Method (call me)
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleRunningOsx(*arg, **kw)

    def PurpleFdGetIp(self, *arg, **kw):
        '''
        Method (call me)
        params:
            fd: INT32
            
        return:
            RESULT: STRING
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleFdGetIp(*arg, **kw)

    def PurpleSocketGetFamily(self, *arg, **kw):
        '''
        Method (call me)
        params:
            fd: INT32
            
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleSocketGetFamily(*arg, **kw)

    def PurpleSocketSpeaksIpv4(self, *arg, **kw):
        '''
        Method (call me)
        params:
            fd: INT32
            
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleSocketSpeaksIpv4(*arg, **kw)

    def PurpleStrequal(self, *arg, **kw):
        '''
        Method (call me)
        params:
            left: STRING
            right: STRING
            
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleStrequal(*arg, **kw)

    def PurpleNormalize(self, *arg, **kw):
        '''
        Method (call me)
        params:
            account: INT32
            str: STRING
            
        return:
            RESULT: STRING
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleNormalize(*arg, **kw)

    def PurpleNormalizeNocase(self, *arg, **kw):
        '''
        Method (call me)
        params:
            account: INT32
            str: STRING
            
        return:
            RESULT: STRING
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleNormalizeNocase(*arg, **kw)

    def PurpleStrHasPrefix(self, *arg, **kw):
        '''
        Method (call me)
        params:
            s: STRING
            p: STRING
            
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleStrHasPrefix(*arg, **kw)

    def PurpleStrHasSuffix(self, *arg, **kw):
        '''
        Method (call me)
        params:
            s: STRING
            x: STRING
            
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleStrHasSuffix(*arg, **kw)

    def PurpleStrdupWithhtml(self, *arg, **kw):
        '''
        Method (call me)
        params:
            src: STRING
            
        return:
            RESULT: STRING
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleStrdupWithhtml(*arg, **kw)

    def PurpleStrAddCr(self, *arg, **kw):
        '''
        Method (call me)
        params:
            str: STRING
            
        return:
            RESULT: STRING
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleStrAddCr(*arg, **kw)

    def PurpleStrreplace(self, *arg, **kw):
        '''
        Method (call me)
        params:
            string: STRING
            delimiter: STRING
            replacement: STRING
            
        return:
            RESULT: STRING
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleStrreplace(*arg, **kw)

    def PurpleUtf8NcrEncode(self, *arg, **kw):
        '''
        Method (call me)
        params:
            in: STRING
            
        return:
            RESULT: STRING
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleUtf8NcrEncode(*arg, **kw)

    def PurpleUtf8NcrDecode(self, *arg, **kw):
        '''
        Method (call me)
        params:
            in: STRING
            
        return:
            RESULT: STRING
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleUtf8NcrDecode(*arg, **kw)

    def PurpleStrcasereplace(self, *arg, **kw):
        '''
        Method (call me)
        params:
            string: STRING
            delimiter: STRING
            replacement: STRING
            
        return:
            RESULT: STRING
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleStrcasereplace(*arg, **kw)

    def PurpleStrcasestr(self, *arg, **kw):
        '''
        Method (call me)
        params:
            haystack: STRING
            needle: STRING
            
        return:
            RESULT: STRING
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleStrcasestr(*arg, **kw)

    def PurpleStrSizeToUnits(self, *arg, **kw):
        '''
        Method (call me)
        params:
            size: INT32
            
        return:
            RESULT: STRING
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleStrSizeToUnits(*arg, **kw)

    def PurpleStrSecondsToString(self, *arg, **kw):
        '''
        Method (call me)
        params:
            sec: INT32
            
        return:
            RESULT: STRING
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleStrSecondsToString(*arg, **kw)

    def PurpleStrBinaryToAscii(self, *arg, **kw):
        '''
        Method (call me)
        params:
            binary: STRING
            len: INT32
            
        return:
            RESULT: STRING
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleStrBinaryToAscii(*arg, **kw)

    def PurpleGotProtocolHandlerUri(self, *arg, **kw):
        '''
        Method (call me)
        params:
            uri: STRING
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleGotProtocolHandlerUri(*arg, **kw)

    def PurpleUtilFetchUrlCancel(self, *arg, **kw):
        '''
        Method (call me)
        params:
            url_data: INT32
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleUtilFetchUrlCancel(*arg, **kw)

    def PurpleUrlDecode(self, *arg, **kw):
        '''
        Method (call me)
        params:
            str: STRING
            
        return:
            RESULT: STRING
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleUrlDecode(*arg, **kw)

    def PurpleUrlEncode(self, *arg, **kw):
        '''
        Method (call me)
        params:
            str: STRING
            
        return:
            RESULT: STRING
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleUrlEncode(*arg, **kw)

    def PurpleEmailIsValid(self, *arg, **kw):
        '''
        Method (call me)
        params:
            address: STRING
            
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleEmailIsValid(*arg, **kw)

    def PurpleIpAddressIsValid(self, *arg, **kw):
        '''
        Method (call me)
        params:
            ip: STRING
            
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleIpAddressIsValid(*arg, **kw)

    def PurpleIpv4AddressIsValid(self, *arg, **kw):
        '''
        Method (call me)
        params:
            ip: STRING
            
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleIpv4AddressIsValid(*arg, **kw)

    def PurpleIpv6AddressIsValid(self, *arg, **kw):
        '''
        Method (call me)
        params:
            ip: STRING
            
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleIpv6AddressIsValid(*arg, **kw)

    def PurpleUriListExtractUris(self, *arg, **kw):
        '''
        Method (call me)
        params:
            uri_list: STRING
            
        return:
            RESULT: as
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleUriListExtractUris(*arg, **kw)

    def PurpleUriListExtractFilenames(self, *arg, **kw):
        '''
        Method (call me)
        params:
            uri_list: STRING
            
        return:
            RESULT: as
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleUriListExtractFilenames(*arg, **kw)

    def PurpleUtf8TryConvert(self, *arg, **kw):
        '''
        Method (call me)
        params:
            str: STRING
            
        return:
            RESULT: STRING
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleUtf8TryConvert(*arg, **kw)

    def PurpleUtf8Salvage(self, *arg, **kw):
        '''
        Method (call me)
        params:
            str: STRING
            
        return:
            RESULT: STRING
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleUtf8Salvage(*arg, **kw)

    def PurpleUtf8StripUnprintables(self, *arg, **kw):
        '''
        Method (call me)
        params:
            str: STRING
            
        return:
            RESULT: STRING
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleUtf8StripUnprintables(*arg, **kw)

    def PurpleUtf8Strcasecmp(self, *arg, **kw):
        '''
        Method (call me)
        params:
            a: STRING
            b: STRING
            
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleUtf8Strcasecmp(*arg, **kw)

    def PurpleUtf8HasWord(self, *arg, **kw):
        '''
        Method (call me)
        params:
            haystack: STRING
            needle: STRING
            
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleUtf8HasWord(*arg, **kw)

    def PurpleTextStripMnemonic(self, *arg, **kw):
        '''
        Method (call me)
        params:
            in: STRING
            
        return:
            RESULT: STRING
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleTextStripMnemonic(*arg, **kw)

    def PurpleUnescapeFilename(self, *arg, **kw):
        '''
        Method (call me)
        params:
            str: STRING
            
        return:
            RESULT: STRING
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleUnescapeFilename(*arg, **kw)

    def PurpleEscapeFilename(self, *arg, **kw):
        '''
        Method (call me)
        params:
            str: STRING
            
        return:
            RESULT: STRING
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleEscapeFilename(*arg, **kw)

    def PurpleOscarConvert(self, *arg, **kw):
        '''
        Method (call me)
        params:
            act: STRING
            protocol: STRING
            
        return:
            RESULT: STRING
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleOscarConvert(*arg, **kw)

    def PurpleRestoreDefaultSignalHandlers(self, *arg, **kw):
        '''
        Method (call me)
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleRestoreDefaultSignalHandlers(*arg, **kw)

    def PurpleGetHostName(self, *arg, **kw):
        '''
        Method (call me)
        return:
            RESULT: STRING
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleGetHostName(*arg, **kw)

    def PurpleUuidRandom(self, *arg, **kw):
        '''
        Method (call me)
        return:
            RESULT: STRING
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleUuidRandom(*arg, **kw)

    def XmlnodeInsertChild(self, *arg, **kw):
        '''
        Method (call me)
        params:
            parent: INT32
            child: INT32
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.XmlnodeInsertChild(*arg, **kw)

    def XmlnodeInsertData(self, *arg, **kw):
        '''
        Method (call me)
        params:
            node: INT32
            data: STRING
            size: INT32
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.XmlnodeInsertData(*arg, **kw)

    def XmlnodeGetData(self, *arg, **kw):
        '''
        Method (call me)
        params:
            node: INT32
            
        return:
            RESULT: STRING
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.XmlnodeGetData(*arg, **kw)

    def XmlnodeGetDataUnescaped(self, *arg, **kw):
        '''
        Method (call me)
        params:
            node: INT32
            
        return:
            RESULT: STRING
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.XmlnodeGetDataUnescaped(*arg, **kw)

    def XmlnodeSetAttrib(self, *arg, **kw):
        '''
        Method (call me)
        params:
            node: INT32
            attr: STRING
            value: STRING
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.XmlnodeSetAttrib(*arg, **kw)

    def XmlnodeSetAttribWithPrefix(self, *arg, **kw):
        '''
        Method (call me)
        params:
            node: INT32
            attr: STRING
            prefix: STRING
            value: STRING
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.XmlnodeSetAttribWithPrefix(*arg, **kw)

    def XmlnodeSetAttribWithNamespace(self, *arg, **kw):
        '''
        Method (call me)
        params:
            node: INT32
            attr: STRING
            xmlns: STRING
            value: STRING
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.XmlnodeSetAttribWithNamespace(*arg, **kw)

    def XmlnodeSetAttribFull(self, *arg, **kw):
        '''
        Method (call me)
        params:
            node: INT32
            attr: STRING
            xmlns: STRING
            prefix: STRING
            value: STRING
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.XmlnodeSetAttribFull(*arg, **kw)

    def XmlnodeGetAttrib(self, *arg, **kw):
        '''
        Method (call me)
        params:
            node: INT32
            attr: STRING
            
        return:
            RESULT: STRING
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.XmlnodeGetAttrib(*arg, **kw)

    def XmlnodeGetAttribWithNamespace(self, *arg, **kw):
        '''
        Method (call me)
        params:
            node: INT32
            attr: STRING
            xmlns: STRING
            
        return:
            RESULT: STRING
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.XmlnodeGetAttribWithNamespace(*arg, **kw)

    def XmlnodeRemoveAttrib(self, *arg, **kw):
        '''
        Method (call me)
        params:
            node: INT32
            attr: STRING
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.XmlnodeRemoveAttrib(*arg, **kw)

    def XmlnodeRemoveAttribWithNamespace(self, *arg, **kw):
        '''
        Method (call me)
        params:
            node: INT32
            attr: STRING
            xmlns: STRING
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.XmlnodeRemoveAttribWithNamespace(*arg, **kw)

    def XmlnodeSetNamespace(self, *arg, **kw):
        '''
        Method (call me)
        params:
            node: INT32
            xmlns: STRING
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.XmlnodeSetNamespace(*arg, **kw)

    def XmlnodeGetNamespace(self, *arg, **kw):
        '''
        Method (call me)
        params:
            node: INT32
            
        return:
            RESULT: STRING
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.XmlnodeGetNamespace(*arg, **kw)

    def XmlnodeSetPrefix(self, *arg, **kw):
        '''
        Method (call me)
        params:
            node: INT32
            prefix: STRING
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.XmlnodeSetPrefix(*arg, **kw)

    def XmlnodeGetPrefix(self, *arg, **kw):
        '''
        Method (call me)
        params:
            node: INT32
            
        return:
            RESULT: STRING
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.XmlnodeGetPrefix(*arg, **kw)

    def XmlnodeToStr(self, *arg, **kw):
        '''
        Method (call me)
        params:
            node: INT32
            len: INT32
            
        return:
            RESULT: STRING
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.XmlnodeToStr(*arg, **kw)

    def XmlnodeToFormattedStr(self, *arg, **kw):
        '''
        Method (call me)
        params:
            node: INT32
            len: INT32
            
        return:
            RESULT: STRING
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.XmlnodeToFormattedStr(*arg, **kw)

    def XmlnodeFree(self, *arg, **kw):
        '''
        Method (call me)
        params:
            node: INT32
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.XmlnodeFree(*arg, **kw)

    def PurpleAttentionTypeNew(self, *arg, **kw):
        '''
        Method (call me)
        params:
            ulname: STRING
            name: STRING
            inc_desc: STRING
            out_desc: STRING
            
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleAttentionTypeNew(*arg, **kw)

    def PurpleAttentionTypeSetName(self, *arg, **kw):
        '''
        Method (call me)
        params:
            type: INT32
            name: STRING
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleAttentionTypeSetName(*arg, **kw)

    def PurpleAttentionTypeSetIncomingDesc(self, *arg, **kw):
        '''
        Method (call me)
        params:
            type: INT32
            desc: STRING
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleAttentionTypeSetIncomingDesc(*arg, **kw)

    def PurpleAttentionTypeSetOutgoingDesc(self, *arg, **kw):
        '''
        Method (call me)
        params:
            type: INT32
            desc: STRING
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleAttentionTypeSetOutgoingDesc(*arg, **kw)

    def PurpleAttentionTypeSetIconName(self, *arg, **kw):
        '''
        Method (call me)
        params:
            type: INT32
            name: STRING
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleAttentionTypeSetIconName(*arg, **kw)

    def PurpleAttentionTypeSetUnlocalizedName(self, *arg, **kw):
        '''
        Method (call me)
        params:
            type: INT32
            ulname: STRING
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleAttentionTypeSetUnlocalizedName(*arg, **kw)

    def PurpleAttentionTypeGetName(self, *arg, **kw):
        '''
        Method (call me)
        params:
            type: INT32
            
        return:
            RESULT: STRING
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleAttentionTypeGetName(*arg, **kw)

    def PurpleAttentionTypeGetIncomingDesc(self, *arg, **kw):
        '''
        Method (call me)
        params:
            type: INT32
            
        return:
            RESULT: STRING
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleAttentionTypeGetIncomingDesc(*arg, **kw)

    def PurpleAttentionTypeGetOutgoingDesc(self, *arg, **kw):
        '''
        Method (call me)
        params:
            type: INT32
            
        return:
            RESULT: STRING
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleAttentionTypeGetOutgoingDesc(*arg, **kw)

    def PurpleAttentionTypeGetIconName(self, *arg, **kw):
        '''
        Method (call me)
        params:
            type: INT32
            
        return:
            RESULT: STRING
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleAttentionTypeGetIconName(*arg, **kw)

    def PurpleAttentionTypeGetUnlocalizedName(self, *arg, **kw):
        '''
        Method (call me)
        params:
            type: INT32
            
        return:
            RESULT: STRING
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleAttentionTypeGetUnlocalizedName(*arg, **kw)

    def PurplePrplGotAccountIdle(self, *arg, **kw):
        '''
        Method (call me)
        params:
            account: INT32
            idle: INT32
            idle_time: INT32
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurplePrplGotAccountIdle(*arg, **kw)

    def PurplePrplGotAccountLoginTime(self, *arg, **kw):
        '''
        Method (call me)
        params:
            account: INT32
            login_time: INT32
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurplePrplGotAccountLoginTime(*arg, **kw)

    def PurplePrplGotAccountActions(self, *arg, **kw):
        '''
        Method (call me)
        params:
            account: INT32
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurplePrplGotAccountActions(*arg, **kw)

    def PurplePrplGotUserIdle(self, *arg, **kw):
        '''
        Method (call me)
        params:
            account: INT32
            name: STRING
            idle: INT32
            idle_time: INT32
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurplePrplGotUserIdle(*arg, **kw)

    def PurplePrplGotUserLoginTime(self, *arg, **kw):
        '''
        Method (call me)
        params:
            account: INT32
            name: STRING
            login_time: INT32
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurplePrplGotUserLoginTime(*arg, **kw)

    def PurplePrplGotUserStatusDeactive(self, *arg, **kw):
        '''
        Method (call me)
        params:
            account: INT32
            name: STRING
            status_id: STRING
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurplePrplGotUserStatusDeactive(*arg, **kw)

    def PurplePrplChangeAccountStatus(self, *arg, **kw):
        '''
        Method (call me)
        params:
            account: INT32
            old_status: INT32
            new_status: INT32
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurplePrplChangeAccountStatus(*arg, **kw)

    def PurplePrplGetStatuses(self, *arg, **kw):
        '''
        Method (call me)
        params:
            account: INT32
            presence: INT32
            
        return:
            RESULT: ai
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurplePrplGetStatuses(*arg, **kw)

    def PurplePrplSendAttention(self, *arg, **kw):
        '''
        Method (call me)
        params:
            gc: INT32
            who: STRING
            type_code: INT32
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurplePrplSendAttention(*arg, **kw)

    def PurplePrplGotAttention(self, *arg, **kw):
        '''
        Method (call me)
        params:
            gc: INT32
            who: STRING
            type_code: INT32
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurplePrplGotAttention(*arg, **kw)

    def PurplePrplGotAttentionInChat(self, *arg, **kw):
        '''
        Method (call me)
        params:
            gc: INT32
            id: INT32
            who: STRING
            type_code: INT32
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurplePrplGotAttentionInChat(*arg, **kw)

    def PurplePrplGetMediaCaps(self, *arg, **kw):
        '''
        Method (call me)
        params:
            account: INT32
            who: STRING
            
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurplePrplGetMediaCaps(*arg, **kw)

    def PurplePrplInitiateMedia(self, *arg, **kw):
        '''
        Method (call me)
        params:
            account: INT32
            who: STRING
            type: INT32
            
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurplePrplInitiateMedia(*arg, **kw)

    def PurplePrplGotMediaCaps(self, *arg, **kw):
        '''
        Method (call me)
        params:
            account: INT32
            who: STRING
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurplePrplGotMediaCaps(*arg, **kw)

    def PurpleFindPrpl(self, *arg, **kw):
        '''
        Method (call me)
        params:
            id: STRING
            
        return:
            RESULT: INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PurpleFindPrpl(*arg, **kw)

    def AccountConnecting(self, callback):
        '''
        Signal (wait for me)
        callback params:
             INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448s
        '''
        self._dbus_interface.connect_to_signal('AccountConnecting', callback)
        return self

    def AccountDisabled(self, callback):
        '''
        Signal (wait for me)
        callback params:
             INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448s
        '''
        self._dbus_interface.connect_to_signal('AccountDisabled', callback)
        return self

    def AccountEnabled(self, callback):
        '''
        Signal (wait for me)
        callback params:
             INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448s
        '''
        self._dbus_interface.connect_to_signal('AccountEnabled', callback)
        return self

    def AccountSettingInfo(self, callback):
        '''
        Signal (wait for me)
        callback params:
             INT32
             INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448s
        '''
        self._dbus_interface.connect_to_signal('AccountSettingInfo', callback)
        return self

    def AccountSetInfo(self, callback):
        '''
        Signal (wait for me)
        callback params:
             INT32
             INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448s
        '''
        self._dbus_interface.connect_to_signal('AccountSetInfo', callback)
        return self

    def AccountCreated(self, callback):
        '''
        Signal (wait for me)
        callback params:
             INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448s
        '''
        self._dbus_interface.connect_to_signal('AccountCreated', callback)
        return self

    def AccountDestroying(self, callback):
        '''
        Signal (wait for me)
        callback params:
             INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448s
        '''
        self._dbus_interface.connect_to_signal('AccountDestroying', callback)
        return self

    def AccountAdded(self, callback):
        '''
        Signal (wait for me)
        callback params:
             INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448s
        '''
        self._dbus_interface.connect_to_signal('AccountAdded', callback)
        return self

    def AccountRemoved(self, callback):
        '''
        Signal (wait for me)
        callback params:
             INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448s
        '''
        self._dbus_interface.connect_to_signal('AccountRemoved', callback)
        return self

    def AccountStatusChanged(self, callback):
        '''
        Signal (wait for me)
        callback params:
             INT32
             INT32
             INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448s
        '''
        self._dbus_interface.connect_to_signal('AccountStatusChanged', callback)
        return self

    def AccountActionsChanged(self, callback):
        '''
        Signal (wait for me)
        callback params:
             INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448s
        '''
        self._dbus_interface.connect_to_signal('AccountActionsChanged', callback)
        return self

    def AccountAliasChanged(self, callback):
        '''
        Signal (wait for me)
        callback params:
             INT32
             INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448s
        '''
        self._dbus_interface.connect_to_signal('AccountAliasChanged', callback)
        return self

    def AccountAuthorizationRequested(self, callback):
        '''
        Signal (wait for me)
        callback params:
             INT32
             INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448s
        '''
        self._dbus_interface.connect_to_signal('AccountAuthorizationRequested', callback)
        return self

    def AccountAuthorizationRequestedWithMessage(self, callback):
        '''
        Signal (wait for me)
        callback params:
             INT32
             INT32
             INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448s
        '''
        self._dbus_interface.connect_to_signal('AccountAuthorizationRequestedWithMessage', callback)
        return self

    def AccountAuthorizationDenied(self, callback):
        '''
        Signal (wait for me)
        callback params:
             INT32
             INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448s
        '''
        self._dbus_interface.connect_to_signal('AccountAuthorizationDenied', callback)
        return self

    def AccountAuthorizationGranted(self, callback):
        '''
        Signal (wait for me)
        callback params:
             INT32
             INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448s
        '''
        self._dbus_interface.connect_to_signal('AccountAuthorizationGranted', callback)
        return self

    def AccountErrorChanged(self, callback):
        '''
        Signal (wait for me)
        callback params:
             INT32
             INT32
             INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448s
        '''
        self._dbus_interface.connect_to_signal('AccountErrorChanged', callback)
        return self

    def AccountSignedOn(self, callback):
        '''
        Signal (wait for me)
        callback params:
             INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448s
        '''
        self._dbus_interface.connect_to_signal('AccountSignedOn', callback)
        return self

    def AccountSignedOff(self, callback):
        '''
        Signal (wait for me)
        callback params:
             INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448s
        '''
        self._dbus_interface.connect_to_signal('AccountSignedOff', callback)
        return self

    def AccountConnectionError(self, callback):
        '''
        Signal (wait for me)
        callback params:
             INT32
             INT32
             INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448s
        '''
        self._dbus_interface.connect_to_signal('AccountConnectionError', callback)
        return self

    def BuddyStatusChanged(self, callback):
        '''
        Signal (wait for me)
        callback params:
             INT32
             INT32
             INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448s
        '''
        self._dbus_interface.connect_to_signal('BuddyStatusChanged', callback)
        return self

    def BuddyPrivacyChanged(self, callback):
        '''
        Signal (wait for me)
        callback params:
             INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448s
        '''
        self._dbus_interface.connect_to_signal('BuddyPrivacyChanged', callback)
        return self

    def BuddyIdleChanged(self, callback):
        '''
        Signal (wait for me)
        callback params:
             INT32
             INT32
             INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448s
        '''
        self._dbus_interface.connect_to_signal('BuddyIdleChanged', callback)
        return self

    def BuddySignedOn(self, callback):
        '''
        Signal (wait for me)
        callback params:
             INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448s
        '''
        self._dbus_interface.connect_to_signal('BuddySignedOn', callback)
        return self

    def BuddySignedOff(self, callback):
        '''
        Signal (wait for me)
        callback params:
             INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448s
        '''
        self._dbus_interface.connect_to_signal('BuddySignedOff', callback)
        return self

    def BuddyGotLoginTime(self, callback):
        '''
        Signal (wait for me)
        callback params:
             INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448s
        '''
        self._dbus_interface.connect_to_signal('BuddyGotLoginTime', callback)
        return self

    def BlistNodeAdded(self, callback):
        '''
        Signal (wait for me)
        callback params:
             INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448s
        '''
        self._dbus_interface.connect_to_signal('BlistNodeAdded', callback)
        return self

    def BlistNodeRemoved(self, callback):
        '''
        Signal (wait for me)
        callback params:
             INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448s
        '''
        self._dbus_interface.connect_to_signal('BlistNodeRemoved', callback)
        return self

    def BuddyAdded(self, callback):
        '''
        Signal (wait for me)
        callback params:
             INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448s
        '''
        self._dbus_interface.connect_to_signal('BuddyAdded', callback)
        return self

    def BuddyRemoved(self, callback):
        '''
        Signal (wait for me)
        callback params:
             INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448s
        '''
        self._dbus_interface.connect_to_signal('BuddyRemoved', callback)
        return self

    def BuddyIconChanged(self, callback):
        '''
        Signal (wait for me)
        callback params:
             INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448s
        '''
        self._dbus_interface.connect_to_signal('BuddyIconChanged', callback)
        return self

    def UpdateIdle(self, callback):
        '''
        Signal (wait for me)
        callback params:
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448s
        '''
        self._dbus_interface.connect_to_signal('UpdateIdle', callback)
        return self

    def BlistNodeExtendedMenu(self, callback):
        '''
        Signal (wait for me)
        callback params:
             INT32
             INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448s
        '''
        self._dbus_interface.connect_to_signal('BlistNodeExtendedMenu', callback)
        return self

    def BlistNodeAliased(self, callback):
        '''
        Signal (wait for me)
        callback params:
             INT32
             INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448s
        '''
        self._dbus_interface.connect_to_signal('BlistNodeAliased', callback)
        return self

    def BuddyCapsChanged(self, callback):
        '''
        Signal (wait for me)
        callback params:
             INT32
             INT32
             INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448s
        '''
        self._dbus_interface.connect_to_signal('BuddyCapsChanged', callback)
        return self

    def CertificateStored(self, callback):
        '''
        Signal (wait for me)
        callback params:
             INT32
             INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448s
        '''
        self._dbus_interface.connect_to_signal('CertificateStored', callback)
        return self

    def CertificateDeleted(self, callback):
        '''
        Signal (wait for me)
        callback params:
             INT32
             INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448s
        '''
        self._dbus_interface.connect_to_signal('CertificateDeleted', callback)
        return self

    def CipherAdded(self, callback):
        '''
        Signal (wait for me)
        callback params:
             INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448s
        '''
        self._dbus_interface.connect_to_signal('CipherAdded', callback)
        return self

    def CipherRemoved(self, callback):
        '''
        Signal (wait for me)
        callback params:
             INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448s
        '''
        self._dbus_interface.connect_to_signal('CipherRemoved', callback)
        return self

    def CmdAdded(self, callback):
        '''
        Signal (wait for me)
        callback params:
             INT32
             INT32
             INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448s
        '''
        self._dbus_interface.connect_to_signal('CmdAdded', callback)
        return self

    def CmdRemoved(self, callback):
        '''
        Signal (wait for me)
        callback params:
             INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448s
        '''
        self._dbus_interface.connect_to_signal('CmdRemoved', callback)
        return self

    def SigningOn(self, callback):
        '''
        Signal (wait for me)
        callback params:
             INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448s
        '''
        self._dbus_interface.connect_to_signal('SigningOn', callback)
        return self

    def SignedOn(self, callback):
        '''
        Signal (wait for me)
        callback params:
             INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448s
        '''
        self._dbus_interface.connect_to_signal('SignedOn', callback)
        return self

    def SigningOff(self, callback):
        '''
        Signal (wait for me)
        callback params:
             INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448s
        '''
        self._dbus_interface.connect_to_signal('SigningOff', callback)
        return self

    def SignedOff(self, callback):
        '''
        Signal (wait for me)
        callback params:
             INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448s
        '''
        self._dbus_interface.connect_to_signal('SignedOff', callback)
        return self

    def ConnectionError(self, callback):
        '''
        Signal (wait for me)
        callback params:
             INT32
             INT32
             INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448s
        '''
        self._dbus_interface.connect_to_signal('ConnectionError', callback)
        return self

    def Autojoin(self, callback):
        '''
        Signal (wait for me)
        callback params:
             INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448s
        '''
        self._dbus_interface.connect_to_signal('Autojoin', callback)
        return self

    def WritingImMsg(self, callback):
        '''
        Signal (wait for me)
        callback params:
             INT32
             INT32
             INT32
             INT32
             UINT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448s
        '''
        self._dbus_interface.connect_to_signal('WritingImMsg', callback)
        return self

    def WroteImMsg(self, callback):
        '''
        Signal (wait for me)
        callback params:
             INT32
             INT32
             INT32
             INT32
             UINT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448s
        '''
        self._dbus_interface.connect_to_signal('WroteImMsg', callback)
        return self

    def SentAttention(self, callback):
        '''
        Signal (wait for me)
        callback params:
             INT32
             INT32
             INT32
             UINT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448s
        '''
        self._dbus_interface.connect_to_signal('SentAttention', callback)
        return self

    def GotAttention(self, callback):
        '''
        Signal (wait for me)
        callback params:
             INT32
             INT32
             INT32
             UINT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448s
        '''
        self._dbus_interface.connect_to_signal('GotAttention', callback)
        return self

    def SendingImMsg(self, callback):
        '''
        Signal (wait for me)
        callback params:
             INT32
             INT32
             INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448s
        '''
        self._dbus_interface.connect_to_signal('SendingImMsg', callback)
        return self

    def SentImMsg(self, callback):
        '''
        Signal (wait for me)
        callback params:
             INT32
             INT32
             INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448s
        '''
        self._dbus_interface.connect_to_signal('SentImMsg', callback)
        return self

    def ReceivingImMsg(self, callback):
        '''
        Signal (wait for me)
        callback params:
             INT32
             INT32
             INT32
             INT32
             INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448s
        '''
        self._dbus_interface.connect_to_signal('ReceivingImMsg', callback)
        return self

    def ReceivedImMsg(self, callback):
        '''
        Signal (wait for me)
        callback params:
             INT32
             INT32
             INT32
             INT32
             UINT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448s
        '''
        self._dbus_interface.connect_to_signal('ReceivedImMsg', callback)
        return self

    def BlockedImMsg(self, callback):
        '''
        Signal (wait for me)
        callback params:
             INT32
             INT32
             INT32
             UINT32
             UINT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448s
        '''
        self._dbus_interface.connect_to_signal('BlockedImMsg', callback)
        return self

    def WritingChatMsg(self, callback):
        '''
        Signal (wait for me)
        callback params:
             INT32
             INT32
             INT32
             INT32
             UINT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448s
        '''
        self._dbus_interface.connect_to_signal('WritingChatMsg', callback)
        return self

    def WroteChatMsg(self, callback):
        '''
        Signal (wait for me)
        callback params:
             INT32
             INT32
             INT32
             INT32
             UINT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448s
        '''
        self._dbus_interface.connect_to_signal('WroteChatMsg', callback)
        return self

    def SendingChatMsg(self, callback):
        '''
        Signal (wait for me)
        callback params:
             INT32
             INT32
             UINT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448s
        '''
        self._dbus_interface.connect_to_signal('SendingChatMsg', callback)
        return self

    def SentChatMsg(self, callback):
        '''
        Signal (wait for me)
        callback params:
             INT32
             INT32
             UINT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448s
        '''
        self._dbus_interface.connect_to_signal('SentChatMsg', callback)
        return self

    def ReceivingChatMsg(self, callback):
        '''
        Signal (wait for me)
        callback params:
             INT32
             INT32
             INT32
             INT32
             INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448s
        '''
        self._dbus_interface.connect_to_signal('ReceivingChatMsg', callback)
        return self

    def ReceivedChatMsg(self, callback):
        '''
        Signal (wait for me)
        callback params:
             INT32
             INT32
             INT32
             INT32
             UINT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448s
        '''
        self._dbus_interface.connect_to_signal('ReceivedChatMsg', callback)
        return self

    def ConversationCreated(self, callback):
        '''
        Signal (wait for me)
        callback params:
             INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448s
        '''
        self._dbus_interface.connect_to_signal('ConversationCreated', callback)
        return self

    def ConversationUpdated(self, callback):
        '''
        Signal (wait for me)
        callback params:
             INT32
             UINT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448s
        '''
        self._dbus_interface.connect_to_signal('ConversationUpdated', callback)
        return self

    def DeletingConversation(self, callback):
        '''
        Signal (wait for me)
        callback params:
             INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448s
        '''
        self._dbus_interface.connect_to_signal('DeletingConversation', callback)
        return self

    def BuddyTyping(self, callback):
        '''
        Signal (wait for me)
        callback params:
             INT32
             INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448s
        '''
        self._dbus_interface.connect_to_signal('BuddyTyping', callback)
        return self

    def BuddyTyped(self, callback):
        '''
        Signal (wait for me)
        callback params:
             INT32
             INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448s
        '''
        self._dbus_interface.connect_to_signal('BuddyTyped', callback)
        return self

    def BuddyTypingStopped(self, callback):
        '''
        Signal (wait for me)
        callback params:
             INT32
             INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448s
        '''
        self._dbus_interface.connect_to_signal('BuddyTypingStopped', callback)
        return self

    def ChatBuddyJoining(self, callback):
        '''
        Signal (wait for me)
        callback params:
             INT32
             INT32
             UINT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448s
        '''
        self._dbus_interface.connect_to_signal('ChatBuddyJoining', callback)
        return self

    def ChatBuddyJoined(self, callback):
        '''
        Signal (wait for me)
        callback params:
             INT32
             INT32
             UINT32
             UINT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448s
        '''
        self._dbus_interface.connect_to_signal('ChatBuddyJoined', callback)
        return self

    def ChatBuddyFlags(self, callback):
        '''
        Signal (wait for me)
        callback params:
             INT32
             INT32
             UINT32
             UINT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448s
        '''
        self._dbus_interface.connect_to_signal('ChatBuddyFlags', callback)
        return self

    def ChatBuddyLeaving(self, callback):
        '''
        Signal (wait for me)
        callback params:
             INT32
             INT32
             INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448s
        '''
        self._dbus_interface.connect_to_signal('ChatBuddyLeaving', callback)
        return self

    def ChatBuddyLeft(self, callback):
        '''
        Signal (wait for me)
        callback params:
             INT32
             INT32
             INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448s
        '''
        self._dbus_interface.connect_to_signal('ChatBuddyLeft', callback)
        return self

    def DeletingChatBuddy(self, callback):
        '''
        Signal (wait for me)
        callback params:
             INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448s
        '''
        self._dbus_interface.connect_to_signal('DeletingChatBuddy', callback)
        return self

    def ChatInvitingUser(self, callback):
        '''
        Signal (wait for me)
        callback params:
             INT32
             INT32
             INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448s
        '''
        self._dbus_interface.connect_to_signal('ChatInvitingUser', callback)
        return self

    def ChatInvitedUser(self, callback):
        '''
        Signal (wait for me)
        callback params:
             INT32
             INT32
             INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448s
        '''
        self._dbus_interface.connect_to_signal('ChatInvitedUser', callback)
        return self

    def ChatInvited(self, callback):
        '''
        Signal (wait for me)
        callback params:
             INT32
             INT32
             INT32
             INT32
             INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448s
        '''
        self._dbus_interface.connect_to_signal('ChatInvited', callback)
        return self

    def ChatInviteBlocked(self, callback):
        '''
        Signal (wait for me)
        callback params:
             INT32
             INT32
             INT32
             INT32
             INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448s
        '''
        self._dbus_interface.connect_to_signal('ChatInviteBlocked', callback)
        return self

    def ChatJoined(self, callback):
        '''
        Signal (wait for me)
        callback params:
             INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448s
        '''
        self._dbus_interface.connect_to_signal('ChatJoined', callback)
        return self

    def ChatJoinFailed(self, callback):
        '''
        Signal (wait for me)
        callback params:
             INT32
             INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448s
        '''
        self._dbus_interface.connect_to_signal('ChatJoinFailed', callback)
        return self

    def ChatLeft(self, callback):
        '''
        Signal (wait for me)
        callback params:
             INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448s
        '''
        self._dbus_interface.connect_to_signal('ChatLeft', callback)
        return self

    def ChatTopicChanged(self, callback):
        '''
        Signal (wait for me)
        callback params:
             INT32
             INT32
             INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448s
        '''
        self._dbus_interface.connect_to_signal('ChatTopicChanged', callback)
        return self

    def ClearedMessageHistory(self, callback):
        '''
        Signal (wait for me)
        callback params:
             INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448s
        '''
        self._dbus_interface.connect_to_signal('ClearedMessageHistory', callback)
        return self

    def ConversationExtendedMenu(self, callback):
        '''
        Signal (wait for me)
        callback params:
             INT32
             INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448s
        '''
        self._dbus_interface.connect_to_signal('ConversationExtendedMenu', callback)
        return self

    def UriHandler(self, callback):
        '''
        Signal (wait for me)
        callback params:
             INT32
             INT32
             INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448s
        '''
        self._dbus_interface.connect_to_signal('UriHandler', callback)
        return self

    def Quitting(self, callback):
        '''
        Signal (wait for me)
        callback params:
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448s
        '''
        self._dbus_interface.connect_to_signal('Quitting', callback)
        return self

    def FileRecvAccept(self, callback):
        '''
        Signal (wait for me)
        callback params:
             INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448s
        '''
        self._dbus_interface.connect_to_signal('FileRecvAccept', callback)
        return self

    def FileSendAccept(self, callback):
        '''
        Signal (wait for me)
        callback params:
             INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448s
        '''
        self._dbus_interface.connect_to_signal('FileSendAccept', callback)
        return self

    def FileRecvStart(self, callback):
        '''
        Signal (wait for me)
        callback params:
             INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448s
        '''
        self._dbus_interface.connect_to_signal('FileRecvStart', callback)
        return self

    def FileSendStart(self, callback):
        '''
        Signal (wait for me)
        callback params:
             INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448s
        '''
        self._dbus_interface.connect_to_signal('FileSendStart', callback)
        return self

    def FileSendCancel(self, callback):
        '''
        Signal (wait for me)
        callback params:
             INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448s
        '''
        self._dbus_interface.connect_to_signal('FileSendCancel', callback)
        return self

    def FileRecvCancel(self, callback):
        '''
        Signal (wait for me)
        callback params:
             INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448s
        '''
        self._dbus_interface.connect_to_signal('FileRecvCancel', callback)
        return self

    def FileSendComplete(self, callback):
        '''
        Signal (wait for me)
        callback params:
             INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448s
        '''
        self._dbus_interface.connect_to_signal('FileSendComplete', callback)
        return self

    def FileRecvComplete(self, callback):
        '''
        Signal (wait for me)
        callback params:
             INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448s
        '''
        self._dbus_interface.connect_to_signal('FileRecvComplete', callback)
        return self

    def FileRecvRequest(self, callback):
        '''
        Signal (wait for me)
        callback params:
             INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448s
        '''
        self._dbus_interface.connect_to_signal('FileRecvRequest', callback)
        return self

    def ImageDeleting(self, callback):
        '''
        Signal (wait for me)
        callback params:
             INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448s
        '''
        self._dbus_interface.connect_to_signal('ImageDeleting', callback)
        return self

    def LogTimestamp(self, callback):
        '''
        Signal (wait for me)
        callback params:
             INT32
             INT64
             BOOLEAN
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448s
        '''
        self._dbus_interface.connect_to_signal('LogTimestamp', callback)
        return self

    def NetworkConfigurationChanged(self, callback):
        '''
        Signal (wait for me)
        callback params:
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448s
        '''
        self._dbus_interface.connect_to_signal('NetworkConfigurationChanged', callback)
        return self

    def DisplayingEmailNotification(self, callback):
        '''
        Signal (wait for me)
        callback params:
             INT32
             INT32
             INT32
             INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448s
        '''
        self._dbus_interface.connect_to_signal('DisplayingEmailNotification', callback)
        return self

    def DisplayingEmailsNotification(self, callback):
        '''
        Signal (wait for me)
        callback params:
             INT32
             INT32
             INT32
             INT32
             UINT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448s
        '''
        self._dbus_interface.connect_to_signal('DisplayingEmailsNotification', callback)
        return self

    def DisplayingUserinfo(self, callback):
        '''
        Signal (wait for me)
        callback params:
             INT32
             INT32
             INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448s
        '''
        self._dbus_interface.connect_to_signal('DisplayingUserinfo', callback)
        return self

    def PluginLoad(self, callback):
        '''
        Signal (wait for me)
        callback params:
             INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448s
        '''
        self._dbus_interface.connect_to_signal('PluginLoad', callback)
        return self

    def PluginUnload(self, callback):
        '''
        Signal (wait for me)
        callback params:
             INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448s
        '''
        self._dbus_interface.connect_to_signal('PluginUnload', callback)
        return self

    def SavedstatusChanged(self, callback):
        '''
        Signal (wait for me)
        callback params:
             INT32
             INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448s
        '''
        self._dbus_interface.connect_to_signal('SavedstatusChanged', callback)
        return self

    def SavedstatusAdded(self, callback):
        '''
        Signal (wait for me)
        callback params:
             INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448s
        '''
        self._dbus_interface.connect_to_signal('SavedstatusAdded', callback)
        return self

    def SavedstatusDeleted(self, callback):
        '''
        Signal (wait for me)
        callback params:
             INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448s
        '''
        self._dbus_interface.connect_to_signal('SavedstatusDeleted', callback)
        return self

    def SavedstatusModified(self, callback):
        '''
        Signal (wait for me)
        callback params:
             INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448s
        '''
        self._dbus_interface.connect_to_signal('SavedstatusModified', callback)
        return self

    def PlayingSoundEvent(self, callback):
        '''
        Signal (wait for me)
        callback params:
             INT32
             INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448s
        '''
        self._dbus_interface.connect_to_signal('PlayingSoundEvent', callback)
        return self

    def IrcSendingText(self, callback):
        '''
        Signal (wait for me)
        callback params:
             INT32
             INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448s
        '''
        self._dbus_interface.connect_to_signal('IrcSendingText', callback)
        return self

    def IrcReceivingText(self, callback):
        '''
        Signal (wait for me)
        callback params:
             INT32
             INT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448s
        '''
        self._dbus_interface.connect_to_signal('IrcReceivingText', callback)
        return self


