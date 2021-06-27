import os
from functools import wraps
from datetime import datetime, timedelta
from django.core.cache import cache

## for pytest
def passTokenTest(next, root, info, **args):
    info.context.passTokenCheck = True
    return next(root, info, **args)


def passToken(next, root, info, **args):
    info.context.passTokenCheck = True
    info.context.uid = 1
    return next(root, info, **args)


def checkToken(resolve_func):
    @wraps(resolve_func)
    def resolve(self, info, **kwargs):
        if hasattr (info.context, 'passTokenCheck'):
            print('I am running test')
            return resolve_func(self, info, **kwargs)
        

        if hasattr (info.context, 'headers') :
            token = info.context.headers.get('authorization')
            uid = cache.get(token, default=None)
            if uid :
                #refresh timeout
                ttl = os.environ['TOKEN_EXPIRE_TIMEOUT']
                cache.set(token, uid, timeout = int(ttl))
                info.context.uid = uid 
                return resolve_func(self, info, **kwargs)
        
        raise Exception('Unauthenticated Access')
    return resolve


def superUserRequired(resolve_func):
    @wraps(resolve_func)
    def resolve(self, info, **kwargs):
        adminKey = info.context.adminKey
        if adminKey == os.environ['SECRET_KEY']:
            print('super user verified')
            return resolve_func(self, info, **kwargs)
        
        raise Exception('Unauthenticated Access')
    return resolve


#can be used if set-cookie is available
def jwt_cookie(view_func):
    @wraps(view_func)
    def wrapped_view(request, *args, **kwargs):
        request.jwt_cookie = True
        expires = datetime.now() + timedelta(seconds=100000)

        response = view_func(request, *args, **kwargs)
        response.set_cookie('_ttk_',
                            'nono',
                            expires=expires,
                            httponly = True)
        return response

    return wrapped_view