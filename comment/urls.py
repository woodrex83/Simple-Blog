from django.conf.urls import re_path
from . import views
from django.urls import path

app_name = "comment"

urlpatterns = [
    #點贊
    path('like/', views.LikeAjax.as_view(), name='like'),
    # 評論
    path('send_comment/', views.CommentAjax.as_view(), name='comment'),
]