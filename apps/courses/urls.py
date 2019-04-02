# _*_ coding:utf-8 _*_
__author__ = 'rapzhang'
__data__ = '2019/4/2 10:50'

from django.conf.urls import url
from .views import CourseListView

urlpatterns = [
    #课程列表页
    url(r'^list/$',CourseListView.as_view(),name='course_list'),


]