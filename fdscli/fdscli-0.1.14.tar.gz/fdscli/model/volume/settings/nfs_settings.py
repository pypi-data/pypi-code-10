from model.volume.settings.volume_settings import VolumeSettings
from model.common.size import Size
from __builtin__ import True


class NfsSettings( VolumeSettings):
    '''
    Created on Nov 10, 2015
    
    @author: nate
    '''
    def __init__(self, use_acls=False, use_root_squash=False, synchronous=False, ip_filters=[], capacity=Size(10, "GB"), block_size=None):
        self.type = "NFS"
        self.capacity = capacity
        self.block_size = block_size
        self.__use_acls = use_acls
        self.__use_root_squash = use_root_squash
        self.__synchronous = synchronous
        self.__ip_filters = ip_filters
        
    def __convert_to_bool(self, value):
        
        if type( value ) is bool:
            return value
        
        if value.lower() in ( "true", "yes", "y", "t" ):
            return True
        
        return False
        
    @property
    def use_acls(self):
        return self.__use_acls
    
    @use_acls.setter
    def use_acls(self, acls):
        self.__use_acls = self.__convert_to_bool( acls )
        
    @property
    def use_root_squash(self):
        return self.__use_root_squash
    
    @use_root_squash.setter
    def use_root_squash(self, root_squash):
        self.__use_root_squash = self.__convert_to_bool( root_squash )
        
    @property
    def synchronous(self):
        return self.__synchronous
    
    @synchronous.setter
    def synchronous(self, sync):
        self.__synchronous= self.__convert_to_bool( sync )
        
    @property
    def ip_filters(self):
        return self.__ip_filters
    
    @ip_filters.setter
    def ip_filters(self, filters):
        self.__ip_filters = filters