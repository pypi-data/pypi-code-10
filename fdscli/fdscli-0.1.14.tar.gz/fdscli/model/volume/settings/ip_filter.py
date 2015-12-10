
class IpFilter(object):
    '''
    Created on Nov 10, 2015
    
    @author: nate
    '''

    def __init__(self, ip_filter=None, mode="ALLOW"):
        self.__ip_filter = ip_filter
        self.__mode = mode
        
    @property 
    def ip_filter(self):
        return self.__ip_filter
    
    @ip_filter.setter
    def ip_filter(self, ip_filter):
        self.__ip_filter = ip_filter

    @property
    def mode(self):
        return self.__mode

    @mode.setter
    def mode(self, mode):
        
        if mode not in ("ALLOW", "DENY"):
            raise TypeError()
        
        self.__mode = mode