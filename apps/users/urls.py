# _*_ coding:utf-8 _*_
__author__ = 'rapzhang'
__data__ = '2019/4/5 23:11'

from django.conf.urls import url,include

from .views import UserInfoView,UploadImageView,UpdatePwdView,SendEmailCodeView,UpdateEmailView
from .views import MyCourseView,MyFavOrgView,MyFavTeacherView,MyFavCourseView,MyMessageView

urlpatterns = [
    # 用户个人中心信息
    url(r'^info/$',UserInfoView.as_view(),name="user_info"),

    # 用户头像上传修改
    url(r'^image/upload/$',UploadImageView.as_view(),name="image_upload"),

    # 用户个人中心修改密码
    url(r'^update/pwd/$', UpdatePwdView.as_view(), name="update_pwd"),

    # 发送邮箱的数字验证码
    url(r'^sendEmail_code/$',SendEmailCodeView.as_view(), name="sendEmail_code"),

    # 验证邮箱的验证码是否和数据库一致
    url(r'^update_email/$', UpdateEmailView.as_view(), name="update_email"),

    # 个人中心我的课程页面
    url(r'^mycourse/$', MyCourseView.as_view(), name="mycourse"),

    # 收藏的课程机构
    url(r'^myfav/org/$', MyFavOrgView.as_view(), name="myfav_org"),

    # 收藏的教师
    url(r'^myfav/teacher/$', MyFavTeacherView.as_view(), name="myfav_teacher"),

    # 收藏的课程
    url(r'^myfav/course/$', MyFavCourseView.as_view(), name="myfav_course"),

    # 我的消息页面
    url(r'^myMessage$', MyMessageView.as_view(), name="myMessage"),

]
