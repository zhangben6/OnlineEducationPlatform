# _*_ coding:utf-8 _*_
__author__ = 'rapzhang'
__data__ = '2019/4/2 10:50'

from django.conf.urls import url
from .views import CourseListView,CourseDetailView,CourseInfoView

urlpatterns = [
    #课程列表页
    url(r'^list/$',CourseListView.as_view(),name='course_list'),

    # 课程详情页
     url(r'^detail/course_id=(?P<course_id>\d+)$', CourseDetailView.as_view(), name='course_detail'),

    # 课程学习页面
    url(r'^info/course_id=(?P<course_id>\d+)$', CourseInfoView.as_view(), name='course_info'),

]