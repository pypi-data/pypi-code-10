import subprocess
from coreinit.utils.exceptions import *
from coreinit.logger import Logger

def install_pip(packages):
    for package in packages:
        Logger.info('Pip install %s' % package)
        r = subprocess.call(['pip',
                             'install',
                             package])
        if r != 0:
            raise ConfigurationException('failed to install %s by pip' % package)

def install_system(packages):
    for package in packages:
        Logger.info('System install %s' % package)
        r = subprocess.call(['apt-get',
                             'install', '--yes', '--force-yes',
                             package])
        if r != 0:
            raise ConfigurationException('failed to install %s by apt-get' % package)