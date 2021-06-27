from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.Blog)
admin.site.register(models.Tag)
admin.site.register(models.Article)
admin.site.register(models.Category)
admin.site.register(models.Article2Tag)
admin.site.register(models.Links)
