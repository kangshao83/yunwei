"""yunwei URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
#coding=utf8
from django.conf.urls import url,include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from app1.views import index as index
from app1.views import run_com as result
from app1.views import user_login as login
from app1.views import user_logout as logout
from app1.views import upload as upload
from app1.views import get_host_list as get_host_list
from app1.api import GroupsResource,HostsResource
from tastypie.api import Api

v1_api = Api(api_name='v1')
v1_api.register(GroupsResource())
v2_api = Api(api_name='v2')
v2_api.register(HostsResource())

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^result/$', result),
    url(r'^login/$', login),
    url(r'^logout/$', logout),
    url(r'^index/$', index),
    url(r'^upload/$', upload),
    url(r'^api/', include(v1_api.urls)),
    #url(r'^api2/', include(v2_api.urls)),
    url(r'^get_host_list/', get_host_list),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
