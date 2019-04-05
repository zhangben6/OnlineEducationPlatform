# _*_ coding:utf-8 _*_
__author__ = 'rapzhang'
__data__ = '2019/4/2 10:50'

from django.conf.urls import url
from .views import CourseListView,CourseDetailView,CourseInfoView,CommentsView,AddCommentView,VideoPlayView

urlpatterns = [
    #课程列表页
    url(r'^list/$',CourseListView.as_view(),name='course_list'),

    # 课程详情页
     url(r'^detail/course_id=(?P<course_id>\d+)$', CourseDetailView.as_view(), name='course_detail'),

    # 课程学习页面
    url(r'^info/course_id=(?P<course_id>\d+)$', CourseInfoView.as_view(), name='course_info'),

    # 课程评论页面
    url(r'^comment/course_id=(?P<course_id>\d+)$', CommentsView.as_view(), name='course_comment'),

    # 前端ajax访问的接口 - 添加用户评论
    url(r'^add_comment/$', AddCommentView.as_view(), name='add_comment'),

    # 视频的url匹配路径
    url(r'^video/video_id=(?P<video_id>\d+)$', VideoPlayView.as_view(), name='video_play'),

]