import datetime
from haystack import indexes
from .models import Article


class ArticleIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    # 每個索引只能有一個字段爲document=True

    desc = indexes.CharField(model_attr='desc')  
    title = indexes.CharField(model_attr='title')  

    # 返回值就是要檢索的對象
    def get_model(self):
        return Article

    def index_queryset(self, using=None):
        return self.get_model().objects.all()