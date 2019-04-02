from django.shortcuts import render
from django.views.generic.base import View
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

from .models import Course
# Create your views here.


class CourseListView(View):
    def get(self,request):
        all_courses = Course.objects.all().order_by('-add_time')

        # 右边导航栏热门课程推荐
        hot_courses = all_courses.order_by('-click_nums')[:3]

        # 按照学习人数和热门课程--- 排序
        sort = request.GET.get('sort', '')
        if sort:
            if sort == 'students':
                all_courses = all_courses.order_by("-students")
            elif sort == 'hot':
                all_courses = all_courses.order_by("-click_nums")

        # 对课程进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        # 为Paginator提供完整查询字符串生成的请求对象
        p = Paginator(all_courses, 9, request=request)
        courses = p.page(page)

        return render(request,'course-list.html',{
            'all_courses':courses,
            'sort':sort,
            'hot_courses':hot_courses
        })


class CourseDetailView(View):
    def get(self,request,course_id):
        course = Course.objects.get(id=int(course_id))


        return render(request,'course-detail.html',{
            'course':course
        })











