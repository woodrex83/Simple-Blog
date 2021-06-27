from django.db import models
from django.contrib.auth.models import AbstractUser
from blog.models import Blog

# 使用django-imagekit可以處理圖片，生成指定大小的縮圖，前端显示src="{{ user.avatar.url }}
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill

class User(AbstractUser):
    nickname = models.CharField(max_length=32, blank=True, null=True, verbose_name='昵稱',unique=True)
    # 用戶頭像,上傳路徑已設置爲media，前端用avatar.url爲media/avatar/...
    avatar = ProcessedImageField(upload_to='avatar',default='avatar/default.png',verbose_name='頭像',
                                processors=[ResizeToFill(100, 100)],    # 處理後的大小
                                format='JPEG',
                                options={'quality': 95}
                                )
    
    # 用戶個人背景圖
    background = models.FileField(upload_to='background',default='background/banner1.png',verbose_name='背景圖')
    
    # to後面需要去掉雙引號！！！否則報錯！！！我找了兩小時
    blog = models.OneToOneField(to=Blog,on_delete=models.CASCADE,null=True,blank=True)

    # 昵稱只能修改一次
    isnickname = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if len(self.avatar.name.split('/')) == 1:
            self.avatar.name = self.username + '/' + self.avatar.name
        #調用父類的save方法後，avatar.name就變成了'upload_to/用户名/文件名'
        super(User, self).save()

    class Meta:
      verbose_name = '用户信息' 
      verbose_name_plural = verbose_name
      ordering = ['-id']
      
    def __str__(self):
      return self.username
