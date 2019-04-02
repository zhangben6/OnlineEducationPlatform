# _*_ coding:utf-8 _*_
__author__ = 'rapzhang'
__data__ = '2019/3/31 12:18'

from django.conf.urls import url
from .views import OrgView,AddUserAskView,OrgHomeView,OrgCourseView,OrgDescView,OrgTeacherView,AddFavView


urlpatterns = [
    #课程机构列表页
    url(r'^list/$',OrgView.as_view(),name='org_list'),

    # 用户咨询
    url(r'^add_ask/$',AddUserAskView.as_view(),name='add_ask'),

    # 机构首页
    url(r'^home/(?P<org_id>\d+)$',OrgHomeView.as_view(),name='org_home'),

    # 机构课程列表页
    url(r'^course/(?P<org_id>\d+)$', OrgCourseView.as_view(), name='org_course'),

    # 课程机构介绍
    url(r'^desc/(?P<org_id>\d+)$', OrgDescView.as_view(), name='org_desc'),

    # 机构教师介绍
    url(r'^teacher/(?P<org_id>\d+)$', OrgTeacherView.as_view(), name='org_teacher'),

    # 机构收藏
    url(r'^add_fav/$',AddFavView.as_view(),name='add_fav')

]