from redis import Redis


class RedisClass(object):
    '''
    Class for caching redis connection
    '''
    _rconn = None
    _settings = None

    def __new__(cls, settings):
        '''
        Instantiate new class
        Args:
            settings (object): settings object for redis info
        '''
        if cls._settings is None:
            cls._settings = settings
            if cls._rconn is None:
                if getattr(cls._settings, 'REDIS_SERVER_AUTH', None):
                    cls._rconn = Redis(host=cls._settings.REDIS_SERVER,
                                       password=cls._settings.REDIS_SERVER_AUTH)
                else:
                    cls._rconn = Redis(host=settings.REDIS_SERVER)
        return super(RedisClass, cls).__new__(cls)

    def __getattr__(self, name):
        '''
        Get attribute from cached redis connection
        Args:
            name (str): name of attribute to get
        '''
        return getattr(self._rconn, name)
