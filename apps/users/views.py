
# Create your views here.
from django.shortcuts import render
from django.contrib.auth import authenticate,login
from django.contrib.auth.backends import ModelBackend
from users.models import UserProfile
from django.db.models import Q
from django.views.generic.base import View


'''重写自定义判断对应的类'''
class CustomBackend(ModelBackend):
    '''重新定义authenticate方法'''
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username)|Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class LoginView(View):
    def get(self,request):
        return render(request, 'login.html', {})
    def post(self,request):
        username = request.POST.get('username', '')
        pass_word = request.POST.get('password', '')
        # 然后再根据数据库进行验证,这时候添加自定义判断
        user = authenticate(username=username, password=pass_word)
        if user is not None:
            login(request, user)
            return render(request, 'index.html')
        else:
            return render(request, 'login.html', {'msg': '用户名密码不正确'})





# Django中FBV实现用户登陆
def user_login(request):
    if request.method == 'GET':
        return render(request,'login.html',{})
    elif request.method == 'POST':
        username = request.POST.get('username','')
        pass_word = request.POST.get('password','')
        # 然后再根据数据库进行验证,这时候添加自定义判断
        user = authenticate(username=username,password=pass_word)
        if user is not None:
            login(request,user) 
            return render(request,'index.html')
        else:
            return render(request,'login.html',{'msg':'用户名密码不正确'})
