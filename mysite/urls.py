"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
<<<<<<< HEAD
=======
from rest_framework import routers
from omok import views
>>>>>>> master
from django.views.decorators.csrf import csrf_exempt
from graphene_django.views import GraphQLView
from mysite.schema import schema

<<<<<<< HEAD

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('admin/', admin.site.urls),
    path('omok_api/', include('omok.urls')),
    path('todo_api/', include('todolist.urls')),
=======
# from mysite import views
router = routers.DefaultRouter()
router.register(r'rooms', views.RoomViewSet)
router.register(r'user',views.UserViewSet)
# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    #path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
>>>>>>> master
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path("graphql/", csrf_exempt(GraphQLView.as_view(graphiql=True, schema=schema))),
]

