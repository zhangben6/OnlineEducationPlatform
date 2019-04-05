# _*_ coding:utf-8 _*_
__author__ = 'rapzhang'
__data__ = '2019/4/5 23:11'

from django.conf.urls import url,include

from .views import UserInfoView
urlpatterns = [
    # 用户个人中心信息
    url(r'^info/$',UserInfoView.as_view(),name="user_info")
]
