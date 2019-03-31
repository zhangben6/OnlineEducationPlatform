# _*_ coding:utf-8 _*_
__author__ = 'rapzhang'
__data__ = '2019/3/31 12:18'

from django.conf.urls import url,include
from .views import OrgView,AddUserAskView


urlpatterns = [
    #课程机构列表页
    url(r'^list/$',OrgView.as_view(),name='org_list'),

    # 用户咨询
    url(r'^add_ask/$',AddUserAskView.as_view(),name='add_ask'),
]