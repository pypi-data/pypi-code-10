import errno
from socket import error as socket_error


def getTileFromCache(cache_location, cache_params, name, key, check, GEVENT_MONKEY_PATCH=False):
    tilecache, tile = get_from_cache(
        cache_location,
        cache_params,
        name,
        key,
        GEVENT_MONKEY_PATCH=GEVENT_MONKEY_PATCH)
    if not tile:
        return tilecache, None

    if check:
        if check_tile_expired(tile):
            print "Tile is expired.  Evicting and returning None"
            tilecache.delete(tile)
            return tilecache, None

    return tilecache, tile


def get_from_cache(cache_location, cache_params, name, key, GEVENT_MONKEY_PATCH=False):
    if GEVENT_MONKEY_PATCH:
        # Import Gevent and monkey patch
        try:
            from gevent import monkey
            monkey.patch_all()
        except:
            print "gevent monkey patch failed"
    # Import Django Cache (mozilla/django-memcached-pool)
    #from django.core.cache import cache, caches, get_cache
    #from django.core.cache import caches
    # Get Tile Cache
    cache = None
    item = None
    try:
        from umemcache import MemcachedError
        from memcachepool.cache import UMemcacheCache
        cache = UMemcacheCache(cache_location, cache_params)
        #cache = caches['tiles']
    except:
        cache = None

    if cache:
        try:
            item = cache.get(key)
	except socket_error, e:
            print e
            item = None        
        except MemcachedError, e:
            print e
            item = None

    return (cache, item)


def check_tile_expired(tile):
    #How to parse HTTP Expires header
    #http://stackoverflow.com/questions/1471987/how-do-i-parse-an-http-date-string-in-python
    import datetime
    expired = False
    now = datetime.datetime.now()
    headers = tile['headers']
    if getValue(headers,'Expires'):
        import email.utils as eut
        #time_expires = datetime.datetime.strptime(getHeader(headers,'Expires'), "%a, %d-%b-%Y %H:%M:%S GMT")
        time_expires = datetime.datetime(*eut.parsedate(getValue(headers,'Expires'))[:6])
        if now >= time_expires:
            expired = True

    return expired

def getValue(d, name, fallback=None):
    value = None
    if d:
        try:
            value = d[name]
        except KeyError:
            value = fallback
    else:
        value = fallback
    return value

def commit_to_cache(cache_location, cache_params, key, obj, GEVENT_MONKEY_PATCH=False):
    if GEVENT_MONKEY_PATCH:
        # Import Gevent and monkey patch
        try:
            from gevent import monkey
            monkey.patch_all()
        except:
            print "gevent monkey patch failed"

    # Import Django Cache (mozilla/django-memcached-pool)
    #from django.core.cache import cache, caches, get_cache
    #from django.core.cache import caches
    # Get Tile Cache
    cache = None
    success = False
    try:
        from umemcache import MemcachedError
        from memcachepool.cache import UMemcacheCache
        cache = UMemcacheCache(cache_location, cache_params)
        #cache = caches['tiles']
    except:
        cache = None

    if cache:
        try:
            cache.set(key, obj)
            success = True
        except MemcachedError, e:
            print e
            success = False

    return success


def check_cache_availability(cache_location, cache_params, GEVENT_MONKEY_PATCH=False):
    if GEVENT_MONKEY_PATCH:
        # Import Gevent and monkey patch
        try:
            from gevent import monkey
            monkey.patch_all()
        except:
            print "gevent monkey patch failed"

    available = False
    cache = None
    try:
        from umemcache import MemcachedError
        from memcachepool.cache import UMemcacheCache
        cache = UMemcacheCache(cache_location, cache_params)
        #cache = caches['tiles']
        #from django.core.cache import caches
        #tilecache = caches[cache]
        cache.get('')
        available = True
    except MemcachedError, e:
        print e
        available = False

    return available

