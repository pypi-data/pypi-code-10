'''
Created with dbus2any

https://github.com/hugosenari/dbus2any


This code require python-dbus

Parameters:

* pydbusclient.tpl
* /org/mpris/MediaPlayer2
* org.mpris.MediaPlayer2.gmusicbrowser

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
        self._dbus_object_path = object_path or "/org/mpris/MediaPlayer2"
        self._dbus_name = bus_name or "org.mpris.MediaPlayer2.gmusicbrowser"

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
            : STRING
            
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
        self._dbus_object_path = object_path or "/org/mpris/MediaPlayer2"
        self._dbus_name = bus_name or "org.mpris.MediaPlayer2.gmusicbrowser"

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

    
    def Get(self, *arg, **kw):
        '''
        Method (call me)
        params:
            : STRING
            : STRING
            
        return:
            : VARIANT
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.Get(*arg, **kw)

    def GetAll(self, *arg, **kw):
        '''
        Method (call me)
        params:
            : STRING
            
        return:
            : a{sv}
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.GetAll(*arg, **kw)

    def Set(self, *arg, **kw):
        '''
        Method (call me)
        params:
            : STRING
            : STRING
            : VARIANT
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.Set(*arg, **kw)

    def PropertiesChanged(self, callback):
        '''
        Signal (wait for me)
        callback params:
             STRING
             a{sv}
             as
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448s
        '''
        self._dbus_interface.connect_to_signal('PropertiesChanged', callback)
        return self


class MediaPlayer2(object):
    '''
    org.mpris.MediaPlayer2

    Usage:
    ------

    Instantiate this class and access the instance members and methods

    >>> obj = MediaPlayer2()

    '''

    def __init__(self, bus_name=None, object_path=None, interface=None, bus=None):
        '''Constructor'''
        self._dbus_interface_name = interface or "org.mpris.MediaPlayer2"
        self._dbus_object_path = object_path or "/org/mpris/MediaPlayer2"
        self._dbus_name = bus_name or "org.mpris.MediaPlayer2.gmusicbrowser"

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

    
    def Quit(self, *arg, **kw):
        '''
        Method (call me)
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.Quit(*arg, **kw)

    def Raise(self, *arg, **kw):
        '''
        Method (call me)
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.Raise(*arg, **kw)

    @property
    def CanQuit(self):
        '''
        Property (acess me)
        Type:
            BOOLEAN read

        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._get_property('CanQuit')
    
    @property
    def CanRaise(self):
        '''
        Property (acess me)
        Type:
            BOOLEAN read

        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._get_property('CanRaise')
    
    @property
    def CanSetFullscreen(self):
        '''
        Property (acess me)
        Type:
            BOOLEAN read

        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._get_property('CanSetFullscreen')
    
    @property
    def DesktopEntry(self):
        '''
        Property (acess me)
        Type:
            STRING read

        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._get_property('DesktopEntry')
    
    @property
    def Fullscreen(self):
        '''
        Property (acess me)
        Type:
            BOOLEAN readwrite

        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._get_property('Fullscreen')
    
    @Fullscreen.setter
    def Fullscreen(self, value):
        self._set_property('Fullscreen', value)
    
    @property
    def HasTrackList(self):
        '''
        Property (acess me)
        Type:
            BOOLEAN read

        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._get_property('HasTrackList')
    
    @property
    def Identity(self):
        '''
        Property (acess me)
        Type:
            STRING read

        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._get_property('Identity')
    
    @property
    def SupportedMimeTypes(self):
        '''
        Property (acess me)
        Type:
            as read

        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._get_property('SupportedMimeTypes')
    
    @property
    def SupportedUriSchemes(self):
        '''
        Property (acess me)
        Type:
            as read

        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._get_property('SupportedUriSchemes')
    

class Player(object):
    '''
    org.mpris.MediaPlayer2.Player

    Usage:
    ------

    Instantiate this class and access the instance members and methods

    >>> obj = Player()

    '''

    def __init__(self, bus_name=None, object_path=None, interface=None, bus=None):
        '''Constructor'''
        self._dbus_interface_name = interface or "org.mpris.MediaPlayer2.Player"
        self._dbus_object_path = object_path or "/org/mpris/MediaPlayer2"
        self._dbus_name = bus_name or "org.mpris.MediaPlayer2.gmusicbrowser"

        bus = bus or dbus.SessionBus()
        self._dbus_object =  bus.get_object(self._dbus_name, self._dbus_object_path)
        self._dbus_interface = dbus.Interface(self._dbus_object,
            dbus_interface=self._dbus_interface_name)
        self._dbus_properties = dbus.Interface(self._dbus_object,
            "org.freedesktop.DBus.Properties")

    def _get_property(self, name):
        return self._dbus_properties.Get(self._dbus_interface_name, name)

    def _set_property(self, name, val):
        return self._dbus_properties.Set(self._dbus_interface_name, name, val)

    
    def Next(self, *arg, **kw):
        '''
        Method (call me)
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.Next(*arg, **kw)

    def OpenUri(self, *arg, **kw):
        '''
        Method (call me)
        params:
            : STRING
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.OpenUri(*arg, **kw)

    def Pause(self, *arg, **kw):
        '''
        Method (call me)
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.Pause(*arg, **kw)

    def Play(self, *arg, **kw):
        '''
        Method (call me)
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.Play(*arg, **kw)

    def PlayPause(self, *arg, **kw):
        '''
        Method (call me)
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.PlayPause(*arg, **kw)

    def Previous(self, *arg, **kw):
        '''
        Method (call me)
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.Previous(*arg, **kw)

    def Seek(self, *arg, **kw):
        '''
        Method (call me)
        params:
            : INT64
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.Seek(*arg, **kw)

    def SetPosition(self, *arg, **kw):
        '''
        Method (call me)
        params:
            : OBJECT_PATH
            : INT64
            
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.SetPosition(*arg, **kw)

    def Stop(self, *arg, **kw):
        '''
        Method (call me)
        
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._dbus_interface.Stop(*arg, **kw)

    def Seeked(self, callback):
        '''
        Signal (wait for me)
        callback params:
             INT64
            
        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448s
        '''
        self._dbus_interface.connect_to_signal('Seeked', callback)
        return self

    @property
    def CanControl(self):
        '''
        Property (acess me)
        Type:
            BOOLEAN read

        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._get_property('CanControl')
    
    @property
    def CanGoNext(self):
        '''
        Property (acess me)
        Type:
            BOOLEAN read

        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._get_property('CanGoNext')
    
    @property
    def CanGoPrevious(self):
        '''
        Property (acess me)
        Type:
            BOOLEAN read

        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._get_property('CanGoPrevious')
    
    @property
    def CanPause(self):
        '''
        Property (acess me)
        Type:
            BOOLEAN read

        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._get_property('CanPause')
    
    @property
    def CanPlay(self):
        '''
        Property (acess me)
        Type:
            BOOLEAN read

        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._get_property('CanPlay')
    
    @property
    def CanSeek(self):
        '''
        Property (acess me)
        Type:
            BOOLEAN read

        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._get_property('CanSeek')
    
    @property
    def LoopStatus(self):
        '''
        Property (acess me)
        Type:
            STRING readwrite

        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._get_property('LoopStatus')
    
    @LoopStatus.setter
    def LoopStatus(self, value):
        self._set_property('LoopStatus', value)
    
    @property
    def MaximumRate(self):
        '''
        Property (acess me)
        Type:
            DOUBLE read

        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._get_property('MaximumRate')
    
    @property
    def Metadata(self):
        '''
        Property (acess me)
        Type:
            a{sv} read

        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._get_property('Metadata')
    
    @property
    def MinimumRate(self):
        '''
        Property (acess me)
        Type:
            DOUBLE read

        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._get_property('MinimumRate')
    
    @property
    def PlaybackStatus(self):
        '''
        Property (acess me)
        Type:
            STRING read

        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._get_property('PlaybackStatus')
    
    @property
    def Position(self):
        '''
        Property (acess me)
        Type:
            INT64 read

        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._get_property('Position')
    
    @property
    def Rate(self):
        '''
        Property (acess me)
        Type:
            DOUBLE readwrite

        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._get_property('Rate')
    
    @Rate.setter
    def Rate(self, value):
        self._set_property('Rate', value)
    
    @property
    def Shuffle(self):
        '''
        Property (acess me)
        Type:
            BOOLEAN readwrite

        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._get_property('Shuffle')
    
    @Shuffle.setter
    def Shuffle(self, value):
        self._set_property('Shuffle', value)
    
    @property
    def Volume(self):
        '''
        Property (acess me)
        Type:
            DOUBLE readwrite

        See also:
            http://dbus.freedesktop.org/doc/dbus-specification.html#idp94392448
        '''
        return self._get_property('Volume')
    
    @Volume.setter
    def Volume(self, value):
        self._set_property('Volume', value)
    

