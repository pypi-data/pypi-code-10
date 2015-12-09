# For Python2 support:
from __future__ import (absolute_import, division,print_function)
from future.standard_library import install_aliases
install_aliases()
from builtins import *
# Needs requests library for HTTP and os library for system calls
import requests
import os

# This srcipt downloads the raasaft/own/, tutorials/ and replication/ 
# directories for raaSAFT into the current directory.

def main():
    # Test for internet
    try:
        requests.head("http://dx.doi.org/")
    except ConnectionError:
        print("Error: you must be connected to the internet.")
        return 1

    # Test for git
    if os.system("git --version") > 0:
        print('Error: please install "git" with your system package manager.')
        return 2
    
    # Print info if person has not cloned from bitbucket before
    print("This will download the raaSAFT directories from Bitbucket.\n")
    print("If you have not used Bitbucket before, you will be asked to trust the host 'bitbucket.org'.\n")
    print("\n")
    
    # "Random" filename for temporary archive
    tarname = "raasaft-j23u9u12.tar"
    
    # Get archive of repo from github
    os.system('git archive --remote=git@bitbucket.org:asmunder/raasaft.git --format=tar --output="'+tarname+'" master')

    # Unpack just the two desired files and folders from archive
    os.system('tar xf '+tarname+' replication tutorials mysaft') 

    # Delete archive and finish
    os.system('rm '+tarname)
    print("Success: raaSAFT folders have been created in this directory.")
    return 0
