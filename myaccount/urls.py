from django.conf.urls import re_path
from . import views

app_name = "myaccount"

urlpatterns = [
    # re_path(r'^profile/$', views.profile, name='profile'),
    re_path(r'^profile/set_avatar/$', views.set_avatar, name='set_avatar'),
    re_path(r'^profile/set_bg/$', views.set_bg, name='set_bg'),
]