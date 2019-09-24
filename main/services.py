import threading
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
import time 
CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)

from django.core.cache import cache, caches
from django.core.cache.backends.base import DEFAULT_TIMEOUT
def cacheUpdate(value,var):
        cache.set('value',var,timeout=CACHE_TTL)
        # time.sleep(20)
        print("Redis Cache Updated")
class CacheUpdateThread(threading.Thread):
    def __init__(self, value, var, *args, **kwargs):
        self.value = value
        self.var = var
        super(CacheUpdateThread, self).__init__(*args, **kwargs)
    
    def run(self):
        cacheUpdate(self.value, self.var)

def memcacheUpdate(value,var):
        caches['memcache'].set('value',var,timeout=CACHE_TTL)
        # time.sleep(20)
        print("Memcache Cache Updated")
class MemCacheUpdateThread(threading.Thread):
    def __init__(self, value, var, *args, **kwargs):
        self.value = value
        self.var = var
        super(MemCacheUpdateThread, self).__init__(*args, **kwargs)
    
    def run(self):
        memcacheUpdate(self.value, self.var)
