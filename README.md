# Blogbuilder 仿博客社區網站

基于`Django`，本質上是個人博客+博客社區系統
![](https://img.shields.io/github/last-commit/WoodRex/DjangoJSBlog)   ![](https://img.shields.io/pypi/pyversions/Django) ![](https://img.shields.io/pypi/djversions/djangorestframework)
## 項目展示

[http://woodrex83.pythonanywhere.com/blog/woodrex83](http://woodrex83.pythonanywhere.com/blog/woodrex83)


## 主要功能

-   注冊/登陸功能
	+ 集合了django-allauth，預設使用google/twitter/discord的Oath
	+ 郵件功能，自動發出注冊帳戶驗證信，找回密碼信件等
-   首頁展示
-   個人博客站點
-   評論功能，包括發表回復評論
-   後台管理
    -   使用kindeditor4.X編輯器，文章及頁面支持`Markdown`



## 運行前注意事項

-   假如要正式配置，不要忘記修改settings.py設置！

```python
SECRET_KEY = ''     # 請自行產生新的key

DEBUG = False

ALLOWED_HOSTS = []  # 這裏要填url

```
-   數據庫使用了django原生sqlite3，如要使用mysql請在settings.py按注解替換

## 本地環境運行
```python
pip install -r requirements.txt
# 如果配置時出錯可以嘗試
# pip install -r requirements.txt --user

python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```
+ 打開http://127.0.0.1:8000/就可以看到效果了

## 創建超級用戶
```python
python3 manage.py createsuperuser
```
+ 創建後可以進入[http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)進行各種設定

### Wechat

ID:生活充滿希望

### discord

ID:Woody#3955
