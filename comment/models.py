from django.db import models
from django.conf import settings
from blog.models import Article


# Create your models here.
class Comment(models.Model):
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    article = models.ForeignKey(to=Article,on_delete=models.CASCADE)
    content = models.CharField(verbose_name='评论内容',max_length=32)
    comment_time = models.DateTimeField(auto_now_add=True)
    # Self-Join（root comment,comments）
    parent = models.ForeignKey(to='self',null=True,on_delete=models.CASCADE)

class Like(models.Model):
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    article = models.ForeignKey(to=Article,on_delete=models.CASCADE)
    is_like = models.BooleanField()