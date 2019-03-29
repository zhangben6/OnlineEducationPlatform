import json

# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate,login
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.views.generic.base import View
from django.contrib.auth.hashers import make_password  # 对明文密码加密
from django.contrib import messages

from users.models import UserProfile,EmailVerifyRecord
from .forms import LoginForm,RegisterForm,ForgetForm,ModifyPwdForm
from utils.email_send import send_register_email


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
        # ret = {'status':200,'msg':'操作成功'}
        # # post请求过来先做前端form表单的验证，然后再查询数据库判断
        # login_form = LoginForm(request.POST)
        # if login_form.is_valid():
        #     username = request.POST.get('username', '')
        #     pass_word = request.POST.get('password', '')
        #     # 然后再根据数据库进行验证,这时候添加自定义判断
        #     user = authenticate(username=username, password=pass_word)
        #     if user is not None:
        #         if user.is_active:
        #             login(request, user)
        #             return HttpResponse(json.dumps(ret))
        #         else:
        #             return render(request,'login.html',{'msg':'用户未激活'})
        #     else:
        #         return render(request, 'login.html', {'msg': '用户名密码不正确'})
        # else:
        #     ret['status'] = -1
        #     ret['msg'] = login_form.errors.as_text()
        #     return HttpResponse(json.dumps(ret))

        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            # 前端格式验证没有错误的话，取出数据
            user_name = request.POST.get('username','')
            pass_word = request.POST.get('password','')
            # 跟数据库做对比
            user = authenticate(username=user_name,password=pass_word)
            if user is not None:
                if user.is_active:
                    login(request,user)  # 这步非常关键
                    return redirect('index')
                else:
                    return render(request,'login.html',{'msg':'用户未被激活'})
            else:
                return render(request,'login.html',{'msg':'用户密码不正确'})
        else:
            return render(request,'login.html',{'login_form':login_form})

class RegisterView(View):
    def get(self,request):
        register_form = RegisterForm()
        return render(request,'register.html',{'register_form':register_form})
    def post(self,request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            # 取出request中的值，保存到数据库
            user_name = request.POST.get('email','')
            if UserProfile.objects.filter(email=user_name):
                return render(request,'login.html',{'register_form':register_form,'msg':"该邮箱已被注册"})
            pass_word = request.POST.get('password','')
            user_profile = UserProfile()
            user_profile.is_active = False
            user_profile.username = user_name
            user_profile.email = user_name
            # 对密码进行加密 django自带功能
            user_profile.password = make_password(pass_word)
            user_profile.save()

            # 发送注册邮件
            send_register_email(user_name,'register')
            return render(request,'login.html')
        else:
            return render(request,'register.html',{'register_form':register_form})

class ActiveUserView(View):
    def get(self,request,active_code):
        # 用户is_active属性激活
        record = EmailVerifyRecord.objects.filter(code=active_code).first()
        if record:
            # 根据record查出用户的email，在userprofile中修改对应的is_active的True状态
            email = record.email
            user = UserProfile.objects.filter(email=email).first()
            user.is_active = True
            user.save()
        else:
            # 目前链接失效的情况，数据库中查不到对应的code
            return render(request,'active_fail.html')

        # 操作成功后不直接返回login页面，为提升用户交互效果，应添加用户交互页面
        return render(request,'active_success.html',{'email':email})

class ForgetPwdView(View):
    def get(self,request):
        forget_form = ForgetForm()
        return render(request,'forgetpwd.html',{'forget_form':forget_form})

    def post(self,request):
        forget_form = ForgetForm(request.POST)
        if forget_form.is_valid():
            # 取出对应的值
            email = request.POST.get('email','')
            user = UserProfile.objects.filter(email=email).first()
            if user:
                # 给用户输入的邮箱发送邮件
                send_register_email(email,'forget')
                return render(request,'send_email_success.html')
            else:
                return render(request,'forgetpwd.html',{'forget_form':forget_form,'msg':'没有对应的用户'})
        else:
            return render(request,'forgetpwd.html',{'forget_form':forget_form})

class ResetView(View):
    def get(self,request,reset_code):
        recode = EmailVerifyRecord.objects.filter(code=reset_code).first()
        email = recode.email
        if recode:
            return render(request,'password_reset.html',{'email':email})
        else:
            return render(request,'active_fail.html')

# 与reset路由接受参数不一致，需要重新定义一个视图类
class ModifyPwdView(View):
    def post(self,request):
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            pwd1 = request.POST.get('password1','')
            pwd2 = request.POST.get('password2','')
            email = request.POST.get('email','')
            if pwd1 != pwd2:
                return render(request,'password_reset.html',{'msg':'两次输入的密码不一致'})
            user = UserProfile.objects.filter(email=email).first()
            user.password = make_password(pwd2)
            user.save()
            return render(request,'login.html')
        else:
            # 保证修改密码界面一直拥有这个属性
            email = request.POST.get('email', '')
            return render(request,'password_reset.html',{'modify_form':modify_form,'email':email})

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
