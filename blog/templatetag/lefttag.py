from django import template
from django.contrib.auth import get_user_model
from blog import models
from django.db.models import Count
from django.db.models.functions import TruncMonth

register = template.Library()

# 自定義inclusion_tag
@register.inclusion_tag('left_menu.html')
def left_menu(nickname):
    # 構造側邊欄需要的數據
    user_obj = get_user_model().objects.filter(nickname=nickname).first()
    blog = user_obj.blog

    # 查詢當前用戶所有分類及分類下的文章數
    category_list = models.Category.objects.filter(blog=blog).annotate(count_num=Count('article__pk')).values_list('name','count_num','pk')

    # 查詢當前用戶所有的標籤及標籤下的文章數
    tag_list = models.Tag.objects.filter(blog=blog).annotate(count_num=Count('article__pk')).values_list('name','count_num','pk')

    # 按照年月統計所有文章
    date_list = models.Article.objects.filter(blog=blog).annotate(month=TruncMonth('create_time')).values('month').annotate(c=Count('pk')).values_list('month','c')

    return locals()