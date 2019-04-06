# _*_ coding:utf-8 _*_
__author__ = 'rapzhang'
__data__ = '2019/4/5 23:11'

from django.conf.urls import url,include

from .views import UserInfoView,UploadImageView,UpdatePwdView
urlpatterns = [
    # 用户个人中心信息
    url(r'^info/$',UserInfoView.as_view(),name="user_info"),

    # 用户头像上传修改
    url(r'^image/upload/$',UploadImageView.as_view(),name="image_upload"),

    # 用户个人中心修改密码
    url(r'^update/pwd/$', UpdatePwdView.as_view(), name="update_pwd")

]
