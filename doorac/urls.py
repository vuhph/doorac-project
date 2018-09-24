from django.conf.urls import url
from . import views

app_name = 'doorac'
urlpatterns = [
    url(r'^$', views.dac_index, name='index'),
    url(r'^login/$', views.dac_login, name='login'),
    url(r'^logout/$', views.dac_logout, name='logout'),
    url(r'^usr/$', views.access_log, name='accesslog'),
    url(r'^usr/list/$', views.user_list, name='usrlist'),
    url(r'^usr/devlog/$', views.user_devlog, name='devlog'),
    url(r'^usr/roomadd/$', views.room_add, name='roomadd'),
    url(r'^webpost$', views.web_post, name='webpost'),
    url(r'^devpost$', views.device_post, name='devpost'),
    url(r'^devupdate$', views.device_update, name='devupdate'),
]
