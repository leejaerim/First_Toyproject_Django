from functools import wraps
from datetime import datetime, timedelta
from toy_auth.models import User


def passTokenTest(next, root, info, **args):
    info.context.passTokenCheck = True
    return next(root, info, **args)


def checkToken(resolve_func):
    @wraps(resolve_func)
    def resolve(self, info, **kwargs):         
        if hasattr (info.context, 'passTokenCheck'):
            print('I am running test')
            info.context.uid = 1
            return resolve_func(self, info, **kwargs)

        if hasattr (info.context, 'headers') :
            token = info.context.headers.get('authorization')
            user = User.objects.filter(token=token).first()
            if user :
                info.context.uid = user.id 
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
        response.set_cookie('__ttk__',
                            'nono',
                            expires=expires,
                            httponly = True)
        return response

    return wrapped_view