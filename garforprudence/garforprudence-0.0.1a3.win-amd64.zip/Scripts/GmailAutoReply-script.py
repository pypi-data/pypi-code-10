#!C:\Python27\python.exe
# EASY-INSTALL-ENTRY-SCRIPT: 'garforprudence==0.0.1a3','console_scripts','GmailAutoReply'
__requires__ = 'garforprudence==0.0.1a3'
import sys
from pkg_resources import load_entry_point

if __name__ == '__main__':
    sys.exit(
        load_entry_point('garforprudence==0.0.1a3', 'console_scripts', 'GmailAutoReply')()
    )
