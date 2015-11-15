'''
Created with dbus2any

https://github.com/hugosenari/dbus2any


This code require python-dbus

Parameters:

* pydbusclient.tpl
* tests/xml/openobex.xml
* /org/openobex/Manager
* org.openobex.Manager

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
        self._dbus_object_path = object_path or "/org/openobex/Manager"
        self._dbus_name = bus_name or "org.openobex.Manager"

        bus = bus or dbus.SessionBus()
        self._dbus_object =  bus.get_object(bus_name, object_path)
        self._dbus_interface = dbus.Interface(self._dbus_object,
            dbus_interface=self._dbus_interface_name)

    
    def Introspect(self, *arg, **kw):
        '''
        Method (call me)
        return:
            data: STRING
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.Introspect(*arg, **kw)


class Properties(object):
    '''
    org.freedesktop.DBus.Properties

    Usage:
    ------

    Instantiate this class and access the instance members and methods

    >>> obj = Properties()

    '''

    def __init__(self, bus_name=None, object_path=None, interface=None, bus=None):
        '''Constructor'''
        self._dbus_interface_name = interface or "org.freedesktop.DBus.Properties"
        self._dbus_object_path = object_path or "/org/openobex/Manager"
        self._dbus_name = bus_name or "org.openobex.Manager"

        bus = bus or dbus.SessionBus()
        self._dbus_object =  bus.get_object(bus_name, object_path)
        self._dbus_interface = dbus.Interface(self._dbus_object,
            dbus_interface=self._dbus_interface_name)

    
    def Get(self, *arg, **kw):
        '''
        Method (call me)
        params:
            interface: STRING
            propname: STRING
            
        return:
            value: VARIANT
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.Get(*arg, **kw)

    def Set(self, *arg, **kw):
        '''
        Method (call me)
        params:
            interface: STRING
            propname: STRING
            value: VARIANT
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.Set(*arg, **kw)

    def GetAll(self, *arg, **kw):
        '''
        Method (call me)
        params:
            interface: STRING
            
        return:
            props: a{sv}
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.GetAll(*arg, **kw)


class Manager(object):
    '''
    org.openobex.Manager

    Usage:
    ------

    Instantiate this class and access the instance members and methods

    >>> obj = Manager()

    '''

    def __init__(self, bus_name=None, object_path=None, interface=None, bus=None):
        '''Constructor'''
        self._dbus_interface_name = interface or "org.openobex.Manager"
        self._dbus_object_path = object_path or "/org/openobex/Manager"
        self._dbus_name = bus_name or "org.openobex.Manager"

        bus = bus or dbus.SessionBus()
        self._dbus_object =  bus.get_object(bus_name, object_path)
        self._dbus_interface = dbus.Interface(self._dbus_object,
            dbus_interface=self._dbus_interface_name)

    
    def GetVersion(self, *arg, **kw):
        '''
        Method (call me)
        return:
            arg0: STRING
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.GetVersion(*arg, **kw)

    def GetServerList(self, *arg, **kw):
        '''
        Method (call me)
        return:
            arg0: as
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.GetServerList(*arg, **kw)

    def GetSessionList(self, *arg, **kw):
        '''
        Method (call me)
        return:
            arg0: as
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.GetSessionList(*arg, **kw)

    def GetServerInfo(self, *arg, **kw):
        '''
        Method (call me)
        params:
            server_object: OBJECT_PATH
            
        return:
            arg1: a{ss}
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.GetServerInfo(*arg, **kw)

    def GetSessionInfo(self, *arg, **kw):
        '''
        Method (call me)
        params:
            session_object: OBJECT_PATH
            
        return:
            arg1: a{ss}
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.GetSessionInfo(*arg, **kw)

    def CreateTtyServer(self, *arg, **kw):
        '''
        Method (call me)
        params:
            tty_dev: STRING
            pattern: STRING
            
        return:
            server_object: OBJECT_PATH
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.CreateTtyServer(*arg, **kw)

    def CreateBluetoothServer(self, *arg, **kw):
        '''
        Method (call me)
        params:
            source_address: STRING
            pattern: STRING
            require_pairing: BOOLEAN
            
        return:
            server_object: OBJECT_PATH
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.CreateBluetoothServer(*arg, **kw)

    def CancelSessionConnect(self, *arg, **kw):
        '''
        Method (call me)
        params:
            session_object: STRING
            
        return:
            arg1: BOOLEAN
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.CancelSessionConnect(*arg, **kw)

    def GetUsbInterfaceInfo(self, *arg, **kw):
        '''
        Method (call me)
        params:
            interface_number: UINT32
            
        return:
            usb_interface: a{ss}
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.GetUsbInterfaceInfo(*arg, **kw)

    def GetUsbInterfacesNum(self, *arg, **kw):
        '''
        Method (call me)
        return:
            interfaces_number: UINT32
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.GetUsbInterfacesNum(*arg, **kw)

    def CreateTtySession(self, *arg, **kw):
        '''
        Method (call me)
        params:
            tty_dev: STRING
            pattern: STRING
            
        return:
            session_object: OBJECT_PATH
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.CreateTtySession(*arg, **kw)

    def CreateUsbSession(self, *arg, **kw):
        '''
        Method (call me)
        params:
            interface_number: UINT32
            pattern: STRING
            
        return:
            session_object: OBJECT_PATH
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.CreateUsbSession(*arg, **kw)

    def CreateBluetoothImagingSession(self, *arg, **kw):
        '''
        Method (call me)
        params:
            target_address: STRING
            source_address: STRING
            bip_feature: STRING
            
        return:
            session_object: OBJECT_PATH
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.CreateBluetoothImagingSession(*arg, **kw)

    def CreateBluetoothSession(self, *arg, **kw):
        '''
        Method (call me)
        params:
            target_address: STRING
            source_address: STRING
            pattern: STRING
            
        return:
            session_object: OBJECT_PATH
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.CreateBluetoothSession(*arg, **kw)

    def SessionConnectError(self, callback):
        '''
        Signal (wait for me)
        callback params:
             OBJECT_PATH
             STRING
             STRING
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448s
        '''
        self._dbus_interface.connect_to_signal('SessionConnectError', callback)
        return self

    def SessionClosed(self, callback):
        '''
        Signal (wait for me)
        callback params:
             OBJECT_PATH
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448s
        '''
        self._dbus_interface.connect_to_signal('SessionClosed', callback)
        return self

    def SessionConnected(self, callback):
        '''
        Signal (wait for me)
        callback params:
             OBJECT_PATH
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448s
        '''
        self._dbus_interface.connect_to_signal('SessionConnected', callback)
        return self


