from django.db import models
from django.utils.html import strip_tags
import markdown

# Create your models here.
class Blog(models.Model):
    site_name = models.CharField(verbose_name='站點名稱',max_length=64,unique=True)
    site_title = models.CharField(verbose_name='站點標題',max_length=32)
    site_theme = models.TextField(verbose_name='站點樣式',null=True,blank=True)

    class Meta:
        verbose_name_plural = '用户站点'
    
    def __str__(self):
        return self.site_name

class Tag(models.Model):
    name = models.CharField(verbose_name='標籤名',max_length=32)
    blog = models.ForeignKey(to='Blog',
                            on_delete=models.CASCADE,
                            null=True)

    class Meta:
        verbose_name_plural = '標籤'
    
    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(verbose_name='分類名',max_length=32)
    blog = models.ForeignKey(to='Blog',on_delete=models.CASCADE,null=True)

    class Meta:
        verbose_name_plural = '分類'
    
    def __str__(self):
        return self.name

class Article(models.Model):
    COMMENT_STATUS = (
        ('o', '打開'),
        ('c', '關閉'),
    )
    title = models.CharField(verbose_name='文章標题',max_length=200)
    desc = models.CharField(verbose_name='文章簡介',max_length=192,blank=True)
    content = models.TextField(verbose_name='文章内容')
    create_time = models.DateTimeField(auto_now_add=True)
    like_num = models.BigIntegerField(verbose_name='點贊数',default=0)
    comment_status = models.CharField(verbose_name='評論狀態',
                                        max_length=1,
                                        choices=COMMENT_STATUS,
                                        default='o')
    comment_num = models.BigIntegerField(verbose_name='評論數',default=0)
    views = models.PositiveIntegerField(verbose_name='瀏覽量',default=0)

    # ForeignKey
    blog = models.ForeignKey(to='Blog',on_delete=models.CASCADE,null=True)

    category = models.ForeignKey(to='Category',
                                on_delete=models.CASCADE,
                                null=True)

    tag = models.ManyToManyField(to='Tag',
                                through='Article2Tag',
                                through_fields=('article','tag'))

    class Meta:
        verbose_name_plural = '文章'
    
    def __str__(self):
        return self.title
    
    def viewed(self):
        self.views += 1
        self.save(update_fields=['views'])
    
    def save(self,*args,**kwargs):
        # 實例化一個markdown類
        # 由於摘要不需要生成文章目錄，去掉了目錄拓展
        md = markdown.Markdown(extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
        ])

        # strip_tags去掉HTML文本的全部HTML標籤，並從文本摘取72個字符
        self.desc = strip_tags(md.convert(self.content))[:72]
        super().save(*args,**kwargs)

class Article2Tag(models.Model):
    article = models.ForeignKey(to='Article',on_delete=models.CASCADE)
    tag = models.ForeignKey(to='Tag',on_delete=models.CASCADE)

class Links(models.Model):
    """同盟頁面"""

    name = models.CharField('鏈接名稱', max_length=30, unique=True)
    link = models.URLField('鏈接地址')
    sequence = models.IntegerField('排序', unique=True)
    is_enable = models.BooleanField('是否显示', default=True, blank=False, null=False)

    class Meta:
        verbose_name_plural = '友情鏈結'

    def __str__(self):
        return self.name

