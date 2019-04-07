import json

# Create your views here.
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render, redirect,reverse
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.views.generic.base import View
from django.contrib.auth.hashers import make_password  # 对明文密码加密
from django.contrib import messages
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger


from users.models import UserProfile,EmailVerifyRecord
from .forms import LoginForm,RegisterForm,ForgetForm,ModifyPwdForm,UserInfoForm
from utils.email_send import send_register_email
from utils.mixin_utils import LoginRequiredMixin
from users.forms import UploadImageForm
from operation.models import UserCourse,UserFavorite,UserMessage
from organization.models import CourseOrg,Teacher
from courses.models import Course
from users.models import Banner


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


class IndexView(View):
    '''Rapzhang在线教育平台首页'''
    def get(self,request):

        # 制造一个异常，出现500页面
        # print(1/0)

        # 取出轮播图
        all_banners = Banner.objects.all().order_by('index')
        # 取出course(非广告位课程)
        courses = Course.objects.filter(is_banner=False)[:6]
        # 取出广告位课程
        banner_courses = Course.objects.filter(is_banner=True)[:3]
        # 取出课程机构
        course_orgs = CourseOrg.objects.all()[:15]

        return render(request,'index.html',{
            'current':'index',
            'all_banners':all_banners,
            'courses':courses,
            'banner_courses':banner_courses,
            'course_orgs':course_orgs
        })

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
                    return redirect(reverse('index'))
                else:
                    return render(request,'login.html',{'msg':'用户未被激活'})
            else:
                return render(request,'login.html',{'msg':'用户密码不正确'})
        else:
            return render(request,'login.html',{'login_form':login_form})


class LogOutView(LoginRequiredMixin,View):
    '''用户推出'''
    def get(self,request):
        logout(request)
        # return redirect(reverse('index'))
        return HttpResponseRedirect(reverse('index'))  # django中的自带重定向函数


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

            # 写入欢迎注册的消息
            user_message = UserMessage()
            user_message.user = user.id
            user.message.message = '欢迎注册Rapzhang在线教育平台，欢迎加入大家庭'
            user.message.save()

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


# 继承了这个LoginRequiredMixin类之后，前端就必须在登陆状态才能访问这个UserInfoView class
class UserInfoView(LoginRequiredMixin,View):
    '''
    用户个人信息
    '''
    def get(self,request):
        return render(request,'usercenter-info.html',{
            'current':'my_info'
        })

    def post(self,request):
        user_info_form = UserInfoForm(request.POST,instance=request.user)
        if user_info_form.is_valid():
            user_info_form.save()
            return HttpResponse(json.dumps({'status': 'success'}), content_type='application/json')

        else:
            return HttpResponse(json.dumps(user_info_form.errors), content_type='application/json')






# 个人中心页面的相关View，都需要加上LoginRequiredMixin，确保用户为登陆状态
class UploadImageView(LoginRequiredMixin,View):
    '''
    用户修改头像
    '''
    # def post(self,request):
    #     '''第一种方法'''
    #     image_form = UploadImageForm(request.POST,request.FILES)
    #     if image_form.is_valid():
    #         image = image_form.cleaned_data['image']
    #         request.user.image = image
    #         request.user.save()
    #         return HttpResponse(json.dumps({'status':'success'}),content_type='application/json')
    #     else:
    #         return HttpResponse(json.dumps({'status': 'fail'}), content_type='application/json')


    '''第二种方法'''
    def post(self,request):
        image_form = UploadImageForm(request.POST,request.FILES,instance=request.user)
        # 因为继承的是ModelForm，所以直接拥有了Model的属性和方法，直接可以save()
        try:
            image_form.save()
            return HttpResponse(json.dumps({'status':'success'}),content_type='application/json')
        except:
            return HttpResponse(json.dumps({'status': 'fail'}), content_type='application/json')


class UpdatePwdView(View):
    '''
    个人中心登陆状态下修改密码
    '''
    def post(self,request):
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            pwd1 = request.POST.get('password1','')
            pwd2 = request.POST.get('password2','')
            if pwd1 != pwd2:
                return HttpResponse(json.dumps({'status': 'fail','msg':'密码不一致'}), content_type='application/json')
            user = request.user
            user.password = make_password(pwd2)
            user.save()
            return HttpResponse(json.dumps({'status': 'success', 'msg': '修改成功'}), content_type='application/json')


        else:
            return HttpResponse(json.dumps(modify_form.errors), content_type='application/json')



class SendEmailCodeView(LoginRequiredMixin,View):
    '''个人中心，发送邮箱验证码'''
    def get(self,request):
        email = request.GET.get('email','')
        if UserProfile.objects.filter(email=email):
            return HttpResponse(json.dumps({'email':'该邮箱已经存在'}),content_type='application/json')
        send_register_email(email,'update_email')
        return HttpResponse(json.dumps({'status': 'success'}), content_type='application/json')


class UpdateEmailView(LoginRequiredMixin,View):
    '''
    修改个人邮箱
    '''
    def post(self,request):
        email = request.POST.get('email','')
        code = request.POST.get('code','')

        existed_records = EmailVerifyRecord.objects.filter(email=email,code=code,send_type='update_email')
        if existed_records:
            user = request.user
            user.email = email
            user.save()
            return HttpResponse(json.dumps({'status':'success'}),content_type='application/json')

        else:
            return HttpResponse(json.dumps({'email':'验证码出错'}),content_type='application/json')


class MyCourseView(LoginRequiredMixin,View):
    '''我的课程'''
    def get(self,request):
        user_courses = UserCourse.objects.filter(user=request.user)
        return render(request,'usercenter-mycourse.html',{
            'user_courses' : user_courses,
            'current':'my_course'
        })



class MyFavOrgView(LoginRequiredMixin,View):
    '''我收藏的课程机构'''
    def get(self,request):
        org_list = []
        fav_orgs = UserFavorite.objects.filter(user=request.user,fav_type=2)
        for fav_org in fav_orgs:
            org_id = fav_org.fav_id
            org = CourseOrg.objects.filter(id=org_id).first()
            org_list.append(org)

        return render(request,'usercenter-fav-org.html',{
            'org_list' : org_list,
        })

class MyFavTeacherView(LoginRequiredMixin,View):
    '''我收藏的教师'''
    def get(self,request):
        teacher_list = []
        fav_teachers = UserFavorite.objects.filter(user=request.user,fav_type=3)
        for fav_teacher in fav_teachers:
            teacher_id = fav_teacher.fav_id
            teacher = Teacher.objects.filter(id=teacher_id).first()
            teacher_list.append(teacher)

        return render(request,'usercenter-fav-teacher.html',{
            'teacher_list' : teacher_list,
        })

class MyFavCourseView(LoginRequiredMixin,View):
    '''我收藏的课程'''
    def get(self,request):
        course_list = []
        fav_courses = UserFavorite.objects.filter(user=request.user,fav_type=1)
        for fav_course in fav_courses:
            course_id = fav_course.fav_id
            course = Course.objects.filter(id=course_id).first()
            print(course.id)
            course_list.append(course)

        return render(request,'usercenter-fav-course.html',{
            'course_list' : course_list,
        })

class MyMessageView(LoginRequiredMixin,View):
    '''我的消息'''
    def get(self,request):
        all_messages = UserMessage.objects.filter(user=request.user.id)

        # 查询用户未读的消息
        all_unread_messages = UserMessage.objects.filter(user=request.user.id,has_read=False)
        for unread_message in all_unread_messages:
            unread_message.has_read = True
            unread_message.save()

        # 对我的消息进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        # 为Paginator提供完整查询字符串生成的请求对象
        p = Paginator(all_messages, 4, request=request)
        messages = p.page(page)

        return render(request,'usercenter-message.html',{
            'messages':messages,
            'current':'my_messages'
        })


# 全局404页面的处理函数
def page_not_found(request):
    from django.shortcuts import render_to_response
    response = render_to_response('404.html',{})
    response.status_code = 404
    return response

# 全局500页面的处理函数
def page_error(request):
    from django.shortcuts import render_to_response
    response = render_to_response('500.html',{})
    response.status_code = 500
    return response


