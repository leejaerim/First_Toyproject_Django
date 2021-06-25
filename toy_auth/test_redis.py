import time 
from django.core.cache import cache


def test_basic():
    cache.set('foo', 'value', timeout=1000)
    result = cache.get('foo')
    timeout = cache.ttl('foo')
    assert result == 'value'
    assert timeout == 1000


def test_ttl():
    cache.set('foo', 'value', timeout=1)
    time.sleep(2)
    result = cache.get('foo')
    assert result is None