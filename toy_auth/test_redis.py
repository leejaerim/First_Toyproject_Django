import time 
from django.core.cache import cache


def test_basic():
    cache.set('foo', 'value', timeout=1000)
    result = cache.get('foo')
    timeout = cache.ttl('foo')
    assert result == 'value'
    assert timeout == 1000


def test_refresh():
    cache.set('foo', 'value', timeout=2)
    assert cache.ttl('foo') == 2
    time.sleep(1)
    assert cache.ttl('foo') == 1
    cache.set('foo', 'value', timeout=3)
    assert cache.ttl('foo') == 3

import os
import binascii

def resolve_token_test():
    ttl = 1
    uid = 1
    def make_token():
        token = binascii.hexlify(os.urandom(20)).decode()
        if cache.add(token, uid, timeout=ttl) :
            return token
        else :
            return make_token()
    key = make_token()

    assert cache.get(key) == 1
    time.sleep(2)
    assert cache.get(key) is None
        
