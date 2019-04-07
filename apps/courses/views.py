import json
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic.base import View
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q

from .models import Course,CourseResource,Video
from operation.models import UserFavorite,CourseComments,UserCourse
from utils.mixin_utils import LoginRequiredMixin
# Create your views here.


class CourseListView(View):
    def get(self,request):
        all_courses = Course.objects.all().order_by('-add_time')

        # 右边导航栏热门课程推荐
        hot_courses = all_courses.order_by('-num_click')[:3]

        # 首页全局导航栏中的关键词字段(课程搜索)
        search_keywords = request.GET.get('keywords','')
        if search_keywords:
            # 对关键词字段进行数据库like查找匹配
            all_courses = all_courses.filter(Q(desc__icontains=search_keywords)|Q(name__icontains=search_keywords)|Q(detail__icontains=search_keywords) )

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
            'hot_courses':hot_courses,
            'current':'course'
        })


class CourseDetailView(View):
    def get(self,request,course_id):
        course = Course.objects.get(id=int(course_id))

        # 取出相关的tag标签，做相关推荐课程
        tag = course.tag
        if tag:
            relate_courses = Course.objects.filter(tag=tag)[:1]
        else:
            relate_courses = []   # 为了让模板中的for循环不报错


        # 每次的点击数 +1
        course.num_click += 1
        course.save()

        # 判断收藏功能的逻辑
        has_fav_course = False
        has_fav_org = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course.id, fav_type=1):
                has_fav_course = True
            if UserFavorite.objects.filter(user=request.user, fav_id=course.course_org.id, fav_type=2):
                has_fav_org = True


        return render(request,'course-detail.html',{
            'course':course,
            'relate_courses':relate_courses,
            'has_fav_course':has_fav_course,
            'has_fav_org':'has_fav_org',
            'current':'course'
        })


class CourseInfoView(LoginRequiredMixin,View):
    '''
    课程章节信息（学习页面)
    '''
    def get(self,request,course_id):
        course = Course.objects.get(id=int(course_id))

        if not UserCourse.objects.filter(user=request.user,course=course):
            course.students += 1
            course.save()

        # 查询用户是否已经关联了该课程（在数据库表中)
        user_course = UserCourse.objects.filter(user=request.user,course=course)
        if not user_course:
            user_course = UserCourse(user=request.user,course=course)
            user_course.save()

        # 查询相关资料
        all_resource = CourseResource.objects.filter(course=course)

        # 用户相关课程推荐:
        # 取出学过这门课的用户们对应的UserCourse对象
        user_courses = UserCourse.objects.filter(course=course)

        # 取出这些对象中的user_id
        user_ids = [user_course.user.id for user_course in user_courses]
        # 取出用户学过的所有课程
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)

        # 取出这些对象中对应的course_id
        course_ids = [user_course.course.id for user_course in all_user_courses]
        # 取出用户们学过的其他相关课程
        relate_courses = Course.objects.filter(id__in=course_ids).order_by('-num_click')[:5]


        return render(request,'course-video.html',{
            'course':course,
            'course_resources':all_resource,
            'relate_courses': relate_courses,
            'current':'course'
        })


class CommentsView(LoginRequiredMixin,View):
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        all_comments = CourseComments.objects.all()
        all_recourse = CourseResource.objects.filter(course=course)


        return render(request, 'course-comment.html', {
            'course': course,
            'all_comments':all_comments,
            'all_recourse':all_recourse,
            'current':'course'
        })


class AddCommentView(View):
    '''
    用户添加课程评论的API
    '''
    def post(self,request):
        if not request.user.is_authenticated():
            return HttpResponse(json.dumps({'status':'fail','msg':'用户未登录'}),content_type='application/json')

        course_id = request.POST.get('course_id',0)
        comments = request.POST.get('comments','')
        if int(course_id) > 0 and comments:
            course = Course.objects.get(id=int(course_id))
            course_comments = CourseComments()
            course_comments.course = course
            course_comments.comments = comments
            course_comments.user = request.user
            course_comments.save()
            return HttpResponse(json.dumps({'status':'success','msg':'添加评论成功'}),content_type='application/json')
        else:
            return HttpResponse(json.dumps({'status':'fail','msg':'添加评论失败'}),content_type='application/json')


class VideoPlayView(View):
    '''
    视频播放页面
    '''
    def get(self,request,video_id):
        video = Video.objects.get(id=int(video_id))
        course = video.lesson.course


        # 查询用户是否已经关联了该课程（在数据库表中)
        user_course = UserCourse.objects.filter(user=request.user,course=course)
        if not user_course:
            user_course = UserCourse(user=request.user,course=course)
            user_course.save()

        # 查询相关资料
        all_resource = CourseResource.objects.filter(course=course)

        # 用户相关课程推荐:
        # 取出学过这门课的用户们对应的UserCourse对象
        user_courses = UserCourse.objects.filter(course=course)

        # 取出这些对象中的user_id
        user_ids = [user_course.user.id for user_course in user_courses]
        # 取出用户学过的所有课程
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)

        # 取出这些对象中对应的course_id
        course_ids = [user_course.course.id for user_course in all_user_courses]
        # 取出用户们学过的其他相关课程
        relate_courses = Course.objects.filter(id__in=course_ids).order_by('-num_click')[:5]


        return render(request,'course-play.html',{
            'course':course,
            'course_resources':all_resource,
            'relate_courses': relate_courses,
            'video':video
        })









