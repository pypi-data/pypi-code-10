from test.base_cli_test import BaseCliTest
from utils.converters.volume.settings_converter import SettingsConverter
import mock_functions
from mock import patch
from model.volume.settings.nfs_settings import NfsSettings
from model.volume.settings.ip_filter import IpFilter
from utils.fds_cli_configuration_manager import FdsCliConfigurationManager

class TestNfsVolume( BaseCliTest ):
    '''
    Created on Nov 9, 2015
    
    @author: nate
    '''

    def test_marshalling(self):
        
        settings = NfsSettings()
        
        settings.use_acls = True
        settings.use_root_squash = False
        settings.synchronous = True
        
        ip_filters = []
        ip_filters.append( IpFilter( ip_filter="localhost*::[0-3]", mode="ALLOW" ) )
        ip_filters.append( IpFilter( ip_filter="12*:abcde[#1]", mode="DENY" ))
        settings.ip_filters = ip_filters
        
        j_str = SettingsConverter.to_json(settings)
        
        print( j_str )
        
        m_settings = SettingsConverter.build_settings_from_json( j_str )
        
        assert m_settings.type == "NFS"
        assert len( m_settings.ip_filters ) == 2
        assert m_settings.ip_filters[0].ip_filter == "localhost*::[0-3]"
        assert m_settings.ip_filters[0].mode == "ALLOW"
        assert m_settings.ip_filters[1].mode == "DENY"
        assert m_settings.ip_filters[1].ip_filter == "12*:abcde[#1]"
        assert settings.use_acls is True
        assert settings.use_root_squash is False
        assert settings.synchronous is True
        
        
    @patch( "services.volume_service.VolumeService.list_volumes", side_effect=mock_functions.listVolumes )
    @patch( "services.volume_service.VolumeService.create_volume", side_effect=mock_functions.createVolume )        
    def test_iscsi_creation(self, volumeCreate, listVolumes ):
        '''
        This test will make sure the settings look right after a volume create call
        '''
        config = FdsCliConfigurationManager()
        config._set_value(FdsCliConfigurationManager.TOGGLES, FdsCliConfigurationManager.NFS, "enabled")
        
        self.cli.loadmodules()
        
        args = ['volume', 'create', '-name', 'nfs', '-type', 'nfs', '-acls', 'true', '-root_squash', 'false', 
                '-ip_filters_allow', 'localhost[1-6]', '-ip_filters_deny', '128.*2*.[6-9]::ab', '10.5.2.255', '-size', 
                '2', '-size_unit', 'TB']
         
        self.callMessageFormatter(args)
        self.cli.run(args)
         
        volume = volumeCreate.call_args[0][0]
        settings = volume.settings
     
        assert settings.type == 'NFS'
        assert len( settings.ip_filters ) == 3
        
        deny_count = 0;
        
        for filt in settings.ip_filters:
            if filt.mode == "DENY":
                deny_count += 1
        
        assert deny_count == 2
        
        assert settings.use_acls is True
        assert settings.use_root_squash is False
        assert settings.synchronous is False
        assert settings.capacity.size == 2
        assert settings.capacity.unit == 'TB'
        
        