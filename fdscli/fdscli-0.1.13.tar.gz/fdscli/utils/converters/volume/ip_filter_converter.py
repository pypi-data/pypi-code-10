import json
from model.volume.settings.ip_filter import IpFilter

class IpFilterConverter(object):
    '''
    Created on Nov 10, 2015
    
    @author: nate
    '''

    @staticmethod
    def to_json( filt ):
        
        j_str = dict()
        
        j_str['ip_filter'] = filt.ip_filter
        j_str['mode'] = filt.mode
        
        j_str = json.dumps( j_str )
        
        return j_str
    
    @staticmethod
    def build_ip_filter_from_json( j_str ):
        
        if not isinstance( j_str, dict ):
            j_str = json.loads(j_str)

        filt = IpFilter()
        
        filt.ip_filter = j_str.pop( 'ip_filter', filt.ip_filter )
        filt.mode = j_str.pop( 'mode', filt.mode )
        
        return filt