from django.conf.urls import re_path
from . import views
from django.urls import path
from haystack.views import SearchView

app_name = "blog"

urlpatterns = [
    re_path(r'^index/', views.IndexView.as_view(), name='index'),
    re_path(r'search/$', SearchView(), name='haystack_search'),
    # 編輯器上傳圖片接口
    # re_path(r'^upload_image/', views.UploadImageView.as_view(), name='upload_image'),
    path('set_nickname/', views.set_nickname, name='swt_nickname'),
    # 後臺管理
    re_path(r'^(?P<nickname>\w+)/backend/', views.BackendView.as_view()),
    # 添加文章
    re_path(r'^(?P<nickname>\w+)/add_article/', views.AddArticleView.as_view()),
    re_path(r'^(?P<nickname>\w+)/article/(?P<article_id>\d+)/article_update', views.ArticleUpdateView.as_view()),
    re_path(r'^(?P<slug1>\w+)/article/(?P<pk>\d+)/delete', views.ArticleDeleteView.as_view()),
    # 文章詳情頁
    re_path(r'^(?P<nickname>\w+)/article/(?P<article_id>\d+)/', views.ArticleDetailView.as_view()),
    re_path(r'^(?P<nickname>\w+)/$', views.SiteView.as_view(), name='site'),
    # 側邊欄篩選功能（三合一）
    re_path(r'^(?P<nickname>\w+)/(?P<condition>category|tag|archive)/(?P<param>.*)/', views.SiteView.as_view()),
]