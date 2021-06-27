from django.shortcuts import render,redirect
from django.http import JsonResponse
from . import models

from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

# 個人信息
# @login_required
# def profile(request):
#     user = request.user
#     return render(request, 'account/profile.html', {'user':user})

# 設置頭像
@login_required
def set_avatar(request):
    username = request.user.username
    user_obj = models.User.objects.filter(username=username).first()

    if request.method == 'POST':
        file_obj = request.FILES.get('avatar')
        # models.User.objects.filter(pk=request.user.pk).update(avatar=file_obj)  # 不會自動加前綴
        if not file_obj:
            file_obj = 'avatar/default.png'
        user_obj.avatar = file_obj
        user_obj.save()
        # return redirect('/'+ username +'/')
        return redirect('/blog/index/')

    return render(request,'account/set_avatar.html',locals())

# 設置背景
def set_bg(request):
    # 需要個人博客開通後才能更換
    nickname = request.user.nickname
    user_obj = models.User.objects.filter(nickname=nickname).first()

    if nickname and request.method == 'POST':
        file_obj = request.FILES.get('bg')
        # models.UserInfo.objects.filter(pk=request.user.pk).update(avatar=file_obj)  # 不會自動加前綴
        if not file_obj:
            user_obj.background = 'background/banner1.png'
            user_obj.save()
        else:
            user_obj.background = file_obj
            user_obj.save()
        # return redirect('/'+ username +'/')
        return redirect('/blog/' + str(nickname) +'/')

    return render(request,'account/set_bg.html',locals())