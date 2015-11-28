# Copyright 2010 Blade Network Technologies

import os, sys, warnings
warnings.simplefilter("ignore", DeprecationWarning)

import get, get_config, edit_config, close_session, copy_config
import delete_config, kill_session, lock, unlock
import get_configuration, get_interface_information

operations = {
    # rfc4741 operations
    'get': get.get,
    'get-config':get_config.get_config,
    'edit-config':edit_config.edit_config,
    'close-session':close_session.close_session,
    'copy-config':copy_config.copy_config,
    'delete-config':delete_config.delete_config,
    'kill-session':kill_session.kill_session,
    'lock':lock.lock,
    'unlock':unlock.unlock,
    # vendor operations
    'get-configuration':get_configuration.get_configuration,
    'get-interface-information':get_interface_information.get_interface_information,
    }

