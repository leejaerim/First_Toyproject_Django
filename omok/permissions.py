from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_permission(self, request,view):
        return bool(request.method in permissions.SAFE_METHODS and request.session.session_key is not None)
    def has_object_permission(self,request,view,obj):
        print(request.user)
        if request.method in permissions.SAFE_METHODS:
            if(request.session.session_key is None):
                request.session.create()
                return False
            else :
                return True




    # if request.COOKIES.get('user') is NOT Null:
    #     user_cookie = request.COOKIES.get('user')
    # request.session['user']=obj.id
    # user = request.session['user']
    #     return true
    # return obj.owner == request.User


    # def session(request):
    # 
    # else :
    #     user_cookie = request.COOKIES.get('user')#session value
    #     user_session = request.session.get('user_id')
    #     User.objects.get()
    #     if 'user' in request.session:
    #     #request.session.session_key 로 user table에서 쿼리
    #     #user가 있으면 user를 response에 넣어서 보내고 아니면 
    #     #새로 session create
    #     pass
    # return HttpResponse()


#         
#         if uesr_cookie == uesr_session
#     elif #not user in COOKIES
#         request.session['user_id']=serializer.data.id #set session
#         request.COOKIES.set_cookie('user',request.session.get('user_id'))

