from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from blog import myutils
from blog.models import Article, Tag, Category, Blog, Article2Tag
from comment import models as cm
from django.contrib.auth import get_user_model
from django.conf import settings
from django.views.generic import ListView, DeleteView
from django.views import View
from django.http import JsonResponse
from django.db.models import F
from django import forms

class IndexView(ListView):
    model = Article
    template_name = 'blog/index.html'
    context_object_name = 'article_list'
    # 等同於queryset = models.Article.objects.all()
    
    page_kwarg = 'page'
    paginate_by = 20

    @property
    def page_number(self):
        page_kwarg = self.page_kwarg
        page = self.kwargs.get(page_kwarg) or self.request.GET.get(page_kwarg) or 1
        return page

# 設置昵稱
@login_required
def set_nickname(request):
    if request.is_ajax():
        back_dic = {'code':2000,'msg':''}

        if request.method == 'POST':
            if request.user.isnickname == False:
                new_nickname = request.POST.get('new_nickname')
                request.user.nickname = new_nickname
                request.user.isnickname = True
                request.user.save()
                back_dic['msg'] = 'Success！'
            else:
                back_dic['msg'] = '昵稱只能修改一次！'
                
        return JsonResponse(back_dic)

# 個人站點
# def site(request,nickname,**kwargs):
#     """
#     kwargs有值，
#     article_list需要進一步篩選condition和param
#     """
#     # 先校驗當前用戶名對應的個人站點是否存在，不存在時返回用戶修改昵稱並通知管理員
#     user_obj = get_user_model().objects.filter(nickname=nickname).first()  
#     if not user_obj:
#         return render(request,'account/blog_inactive.html')

#     blog = user_obj.blog

#     # 查詢當前個人站點
#     article_list = Article.objects.filter(blog=blog)
#     if kwargs:
#         condition = kwargs.get('condition')
#         param = kwargs.get('param')
#         if condition == 'category':
#             article_list = article_list.filter(category_id=param)
#         elif condition == 'tag':
#             article_list = article_list.filter(tag__id=param)
#         else:
#             year, month = param.split('-')
#             article_list = article_list.filter(create_time__year=year,create_time__month=month)

#     # 分頁器
#     current_page = request.GET.get('page',1)
#     all_count = article_list.count()
#     # 傳值生成對象
#     page_obj = myutils.Pagination(current_page=current_page,all_count=all_count)
#     page_queryset = article_list[page_obj.start:page_obj.end]

#     return render(request,'blog/site.html',locals())

# 個人站點
class SiteView(ListView):
    # model = Article
    template_name = 'blog/site.html'
    context_object_name = 'user_obj'
    
    def get_queryset(self):
        # 獲取當前網頁用戶信息
        nickname = self.kwargs.get('nickname')
        user_obj = get_user_model().objects.filter(nickname=nickname).first()

        if not user_obj:
            return render(self.request,'account/blog_inactive.html')
            
        # 封裝！
        user_obj.article_list = Article.objects.filter(blog=user_obj.blog).order_by('-create_time')

        article_list = user_obj.article_list

        if self.kwargs:
            condition = self.kwargs.get('condition')
            param = self.kwargs.get('param')
            if condition == 'category':
                user_obj.article_list = article_list.filter(category_id=param).order_by('-create_time')
            elif condition == 'tag':
                user_obj.article_list = article_list.filter(tag__id=param).order_by('-create_time')
            elif condition == 'archive':
                year, month = param.split('-')
                user_obj.article_list = article_list.filter(create_time__year=year,create_time__month=month).order_by('-create_time')
        
        # 分頁器
        current_page = self.request.GET.get('page',1)
        all_count = article_list.count()
        # 封！都給我封！傳值生成對象
        user_obj.page_obj = myutils.Pagination(current_page=current_page,all_count=all_count)
        user_obj.page_queryset = article_list[user_obj.page_obj.start:user_obj.page_obj.end]
        
        return user_obj
    
    # 硬着頭皮寫出來的跳轉
    def render_to_response(self, context, **kwargs):
        nickname = self.kwargs.get('nickname')
        user_obj = get_user_model().objects.filter(nickname=nickname).first()
        if not user_obj:
            return render(self.request,'account/blog_inactive.html')
        return super().render_to_response(context)

# 文章詳情頁面
import markdown
class ArticleDetailView(View):

    def get(self, request, *args, **kwargs):
        # 文章對象
        article_id = self.kwargs.get('article_id')
        nickname = self.kwargs.get('nickname')
        user_obj = get_user_model().objects.filter(nickname=nickname).first()
        article_obj = Article.objects.filter(pk=article_id,blog__user__nickname=nickname).first()
        article_obj.content = markdown.markdown(article_obj.content,
                                    extensions=[
                                        'markdown.extensions.extra',
                                        'markdown.extensions.codehilite',
                                        'markdown.extensions.toc',
                                    ])

        # if not article_obj:
        #     return render(self.request,'errors.html')    # 404

        # 將文章閱讀量+1
        article_obj.viewed()
        
        # 獲取當前文章的評論內容
        comment_list = cm.Comment.objects.filter(article=article_obj)
        return render(self.request,'blog/article_detail.html',locals())

# 個人後臺
from django.utils.decorators import method_decorator
from django.utils.decorators import method_decorator
@method_decorator(login_required, name='dispatch')
class BackendView(ListView):
    model = Article
    template_name = 'blog/backend/article_list.html'
    # context_object_name = 'article_list'
    
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        nickname = self.kwargs.get('nickname')
        user_obj = get_user_model().objects.filter(nickname=nickname).first()
        article_list = Article.objects.filter(blog=user_obj.blog)
        context['article_list'] = article_list
        context['user_obj'] = user_obj
        # 分頁器
        current_page = self.request.GET.get('page',1)
        all_count = article_list.count()
        page_obj = myutils.Pagination(current_page=current_page,all_count=all_count)
        context['page_obj'] = page_obj
        context['page_queryset'] = article_list[page_obj.start:page_obj.end]
        return context

from bs4 import BeautifulSoup
@method_decorator(login_required, name='dispatch')
class AddArticleView(View):
    def get(self, *args, **kwargs):
        nickname = self.kwargs.get('nickname')
        user_obj = get_user_model().objects.filter(nickname=nickname).first()
        if not user_obj.blog:
            return render(self.request,'account/blog_inactive.html')
        category_list = Category.objects.filter(blog=user_obj.blog)
        tag_list = Tag.objects.filter(blog=user_obj.blog)
        return render(self.request,'blog/backend/add_article.html',locals())

    def post(self, *args, **kwargs):
        title = self.request.POST.get('title')
        content = self.request.POST.get('content')
        category_id = self.request.POST.get('category')
        tag_id_list = self.request.POST.getlist('tag')

        # 標題不能爲空白
        if not title:
            return render(self.request,'blog/backend/error.html',locals())
        # 使用bs4防止xss攻擊(其實在model已經變成markdown)
        soup = BeautifulSoup(content,'html.parser')
        # 獲取所有的標籤
        tags = soup.find_all()
        for tag in tags:
            # 針對script標籤直接刪除
            if tag.name == 'script':
                tag.decompose()
        
        # 文章簡介desc已經在model表自動處理完，不用處理
        # desc = content[0:150]
        article_obj = Article.objects.create(
            title=title,
            content=str(soup),
            # desc=desc
            category_id=category_id,
            blog=self.request.user.blog,
        )

        # Article2Tag表沒法使用add/set/remove/clear
        # 自己操作關系表 一次性可能添加多條數據（批量插入bulk_create）
        article_obj_list = []
        for i in tag_id_list:
            article_obj_list.append(Article2Tag(article=article_obj,tag_id=i))
        
        # 批量插入
        Article2Tag.objects.bulk_create(article_obj_list)

        # 跳轉到後臺管理文章的展示頁
        return redirect('/blog/'+ self.request.user.nickname +'/backend/')

# 文章刪除
@method_decorator(login_required, name='dispatch')
class ArticleDeleteView(DeleteView):
    model = Article
    success_url = ''

    # def get_object(self, queryset=None):
    #     obj = super(ArticleDeleteView, self).get_object(queryset=queryset)
    #     if obj.author != self.request.user:
    #         raise Http404()
    #     return obj

    def post(self, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        data = {'success': 'OK'}
        return JsonResponse(data)

# 文章修改(待優化)
@method_decorator(login_required, name='dispatch')
class ArticleUpdateView(View):
    def get(self, *args, **kwargs):
        nickname = self.kwargs.get('nickname')
        user_obj = get_user_model().objects.filter(nickname=nickname).first()
        category_list = Category.objects.filter(blog=user_obj.blog)
        tag_list = Tag.objects.filter(blog=user_obj.blog)
        article = Article.objects.filter(blog=user_obj.blog,pk=self.kwargs.get('article_id')).first()
        return render(self.request,'blog/backend/article_update.html',locals())
    
    def post(self, *args, **kwargs):
        title = self.request.POST.get('title')
        content = self.request.POST.get('content')
        category_id = self.request.POST.get('category')
        tag_id_list = self.request.POST.getlist('tag')

        nickname = self.kwargs.get('nickname')
        user_obj = get_user_model().objects.filter(nickname=nickname).first()
        
        # 標題不能爲空白
        if not title:
            return render(self.request,'blog/backend/error.html',locals())
        # 使用bs4防止xss攻擊(其實在model已經變成markdown)
        soup = BeautifulSoup(content,'html.parser')
        # 獲取所有的標籤
        tags = soup.find_all()
        for tag in tags:
            # 針對script標籤直接刪除
            if tag.name == 'script':
                tag.decompose()
    
        article_obj = Article.objects.filter(blog=user_obj.blog,pk=self.kwargs.get('article_id')).update(
            title=title,
            blog=self.request.user.blog,
            content=str(soup),
        )

        # 跳轉到後臺管理文章的展示頁
        return redirect('/blog/'+ self.request.user.nickname +'/backend/')


"""
爲安全起見，不開放上傳文件功能
"""
# import os
# class UploadImageView(View):
#     def post(self, *args, **kwargs):
#         # 必須返回要求的JSON格式
#         # 用戶上傳的圖片 也算靜態資源 應該放在media文件夾（以後nginx會動靜分離，靜態放到nginx）
#         back_dic = {'error':0,'url':''} # 提前定義返回給編輯器的數據格式
#         file_obj = self.request.FILES.get('imgFile')
#         file_name = file_obj.name

#         # 確定傳送種類
#         img_format_list = ['jpg','bng','png','gif','jpeg']
#         if file_name.split('.')[-1] in img_format_list:
#             # 手動拼接保存路徑
#             file_dir = os.path.join(settings.BASE_DIR,'media','article_img')
#             if not os.path.isdir(file_dir):
#                 os.mkdir(file_dir)
#             # 拼接完整路徑
#             file_path = os.path.join(file_dir,file_name)
#             with open(file_path,'wb') as f:
#                 for line in file_obj:
#                     f.write(line)
#             back_dic['url'] = '/media/article_img/%s' % file_obj.name
        
#         else:
#             back_dic = {'error':1,'message':'請上傳圖片！'}
    
#         return JsonResponse(back_dic)