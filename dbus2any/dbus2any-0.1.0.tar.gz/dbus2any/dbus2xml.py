# -*- coding: utf-8 -*-
import dbus



def createDbusProxyObject(bus_name, object_path, bus=None):
    '''
    Create dbus proxy object
    '''
    bus = bus or dbus.SessionBus.get_session()
    return bus.get_object(bus_name, object_path)


def fetchXMLFromDbusObject(obj):
    '''
    Return xml of dbus proxy object
    '''
    method = obj.get_dbus_method("Introspect", dbus_interface="org.freedesktop.DBus.Introspectable")
    return method()


def dbus2xml(bus_name, object_path, bus=None):
    obj = createDbusProxyObject(bus_name, object_path, bus)
    return fetchXMLFromDbusObject(obj)