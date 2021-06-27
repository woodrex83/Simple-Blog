from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
from django.db import transaction
from blog.models import Article
from .models import Comment, Like


from django.db.models import F
class CommentAjax(View):
    def post(self, *args, **kwargs):
        if self.request.method == 'POST' and self.request.is_ajax():
            back_dic = {'code':1000,'msg':""}
            if self.request.user.is_authenticated:
                article_id = self.request.POST.get('article_id')
                content = self.request.POST.get('content')
                parent_id = self.request.POST.get('parent_id')

                # 防止空白評論
                if len(content):
                    # 事務操作評論表 存儲數據
                    with transaction.atomic():
                        Article.objects.filter(pk=article_id).update(comment_num=F('comment_num')+1)
                        Comment.objects.create(user=self.request.user,article_id=article_id,content=content,parent_id=parent_id)
                    back_dic['msg'] = '評論成功！'

            else:
                back_dic['code'] = 1002
                back_dic['msg'] = '用戶未登錄'
        return JsonResponse(back_dic)

import json
class LikeAjax(View):
    """
    1.檢驗用戶是否登陸
    2.判斷當前文章是否用戶自己寫的
    3.當前用戶是否已經給當前文章點過了
    4.操作數據庫
    """
    def post(self, *args, **kwargs):
        if self.request.method == 'POST' and self.request.is_ajax():
            back_dic = {'code':1000,'msg':""}
            # 1 判斷當前用戶是否登陸
            if self.request.user.is_authenticated:
                article_id = self.request.POST.get('article_id')
                is_like = self.request.POST.get('is_like')   # 雖然是boolean,但本身class仍是str
                is_like = json.loads(is_like)  # 記得轉換

                # 2 根據當前文章id判斷是否用戶自己寫的，跟request.user比對
                article_obj = Article.objects.filter(pk=article_id).first()
                if not article_obj.blog.user == self.request.user:
                    # 3 校驗當前用戶是否已經點了
                    is_click = Like.objects.filter(user=self.request.user,article=article_obj)
                    if not is_click:
                        # 4 操作數據庫記錄數據
                        Article.objects.filter(pk=article_id).update(like_num=F('like_num')+1)
                        back_dic['msg'] = '點贊成功'
                        Like.objects.create(user=request.user,article=article_obj,is_like=is_like)
                    else:
                        back_dic['code'] = 1001
                        back_dic['msg'] = '已經點贊了'
                else:
                    back_dic['code'] = 1002
                    back_dic['msg'] = '不能自己給自己點贊'
            else:
                back_dic['code'] = 1003
                back_dic['msg'] = '請先<a href="/accounts/login/">登陸</a>'
            return JsonResponse(back_dic)