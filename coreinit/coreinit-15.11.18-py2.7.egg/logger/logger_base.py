class LoggerBase(object):
    '''
    Base class for logging service. To enable logger via DEFAULT_LOGGER, the child
    class should be named Logger.
    '''

    def configure(self):
        pass

    def debug(self, msg='', exception=None):
        pass

    def info(self, msg='', exception=None):
        pass

    def warning(self, msg='', exception=None):
        pass

    def error(self, msg='', exception=None):
        pass

    def crit(self, msg='', exception=None):
        pass