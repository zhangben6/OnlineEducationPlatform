# _*_ coding: utf-8 _*_
__author__ = 'rapzhang'
__date__ = '2019/3/2 12:37'

import xadmin
from .models import Course,Lesson,Video,CourseResource,BannerCourse

class LessonInLine(object):
    model = Lesson
    extra = 0


class CourseAdmin(object):
    list_display = ['course_org','name', 'desc', 'detail', 'degree', 'learn_times','students','fav_nums','image','num_click','add_time']
    search_fields = ['course_org','name', 'desc', 'detail', 'degree','students','fav_nums','image','num_click']
    list_filter = ['course_org','name', 'desc', 'detail', 'degree', 'learn_times','students','fav_nums','image','num_click','add_time']
    ordering = ['-num_click']
    readonly_fields = ['num_click','fav_nums']
    inlines = [LessonInLine]

    def queryset(self):
         qs = super(CourseAdmin,self).queryset()
         qs = qs.filter(is_banner=False)
         return qs

# 为轮播图功能专门设计的一个类
class BannerCourseAdmin(object):
    list_display = ['course_org','name', 'desc', 'detail', 'degree', 'learn_times','students','fav_nums','image','num_click','add_time']
    search_fields = ['course_org','name', 'desc', 'detail', 'degree','students','fav_nums','image','num_click']
    list_filter = ['course_org','name', 'desc', 'detail', 'degree', 'learn_times','students','fav_nums','image','num_click','add_time']
    ordering = ['-num_click']
    readonly_fields = ['num_click','fav_nums']
    inlines = [LessonInLine]

    def queryset(self):
         qs = super(BannerCourseAdmin,self).queryset()
         qs = qs.filter(is_banner=True)
         return qs


class LessonAdmin(object):
    list_display = ['course', 'name', 'add_time']
    search_fields =['course', 'name']
    list_filter = ['course__name', 'name', 'add_time']


class VideoAdmin(object):
    list_display = ['lesson', 'name', 'add_time']
    search_fields = ['lesson', 'name']
    list_filter = ['lesson', 'name', 'add_time']


class CourseResourceAdmin(object):
    list_display = ['course', 'name','download','add_time']
    search_fields = ['course', 'name','download']
    list_filter = ['course__name', 'name','download','add_time']


xadmin.site.register(Course,CourseAdmin)
xadmin.site.register(BannerCourse,BannerCourseAdmin)

xadmin.site.register(Lesson,LessonAdmin)
xadmin.site.register(Video,VideoAdmin)
xadmin.site.register(CourseResource,CourseResourceAdmin)