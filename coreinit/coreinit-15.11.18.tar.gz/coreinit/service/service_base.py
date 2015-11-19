from coreinit.logger import Logger
from coreinit.utils import template

class ServiceBase(object):
    service_name = 'undefined'

    def configure(self):
        Logger.configure(self.service_name)
        template.configure()


    def startup(self):
        pass

    def cleanup(self):
        pass