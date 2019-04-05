import json

from django.shortcuts import render
from django.views.generic import View
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse,JsonResponse
from django.db.models import Q
# Create your views here.

from .models import CourseOrg,CityDict,Teacher
from .forms import UserAskForm
from courses.models import Course
from operation.models import UserFavorite


class OrgView(View):
    '''
    课程机构列表功能
    '''
    def get(self,request):
        # 所有的城市和课程机构
        all_orgs = CourseOrg.objects.all()

        # 网页右边课程机构的排名展示
        hot_orgs = all_orgs.order_by("-click_num")[:6]

        all_citys = CityDict.objects.all()

        # 首页全局导航栏中的关键词字段(课程搜索)
        search_keywords = request.GET.get('keywords', '')
        if search_keywords:
            # 对关键词字段进行数据库like查找匹配
            all_orgs = all_orgs.filter(
                Q(desc__icontains=search_keywords) | Q(name__icontains=search_keywords))

        # 取出筛选城市 city_id
        city_id = request.GET.get('city', '')
        if city_id:
            all_orgs = all_orgs.filter(city_id=int(city_id))

        # 类别机构筛选
        category = request.GET.get('ct', '')
        if category:
            all_orgs = all_orgs.filter(category=category)

        # 按照学习人数和课程数进行sort排序
        sort = request.GET.get('sort','')
        if sort:
            if sort == 'students':
                all_orgs = all_orgs.order_by("-students")
            elif sort == 'courses':
                all_orgs = all_orgs.order_by("-course_nums")

        # 对课程机构进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        # 为Paginator提供完整查询字符串生成的请求对象
        p = Paginator(all_orgs,5,request=request)
        orgs = p.page(page)

        # QuerySet类型可以直接用count()统计数量
        org_nums = all_orgs.count()

        return render(request,'org-list.html',{
            'all_orgs':orgs,
            'all_citys':all_citys,
            'org_nums':org_nums,
            'city_id':city_id,
            'category':category,
            'hot_orgs':hot_orgs,
            'sort':sort,
            'current':'org',
        })


class AddUserAskView(View):
    '''
    用户添加咨询
    '''
    def post(self,request):
        userAsk_form = UserAskForm(request.POST)
        if userAsk_form.is_valid():
            user_ask = userAsk_form.save(commit=True)
            return HttpResponse(json.dumps({'status':'success'}),content_type='application/json')
        else:
            msg = {'status':'fail','msg':'add false'}
            # return HttpResponse(json.dumps({'status':'fail','msg':'添加出错'},ensure_ascii=False),content_type='application/json,charset=utf-8')
            return JsonResponse({'status':'fail','msg':'添加出错1'})


class OrgHomeView(View):
    '''
    机构首页
    '''
    def get(self,request,org_id):
        # 取出对应的课程机构
        course_org = CourseOrg.objects.get(id=int(org_id))

        # 根据外键取出所有的课程
        all_courses = course_org.course_set.all()[:4]
        all_teachers = course_org.teacher_set.all()[:2]

        # 收藏功能判断用户是否登陆
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user,fav_id=course_org.id,fav_type=2):
                has_fav = True

        # 这个值用于org_base.html页面的选中做铺垫
        current_page = 'home'
        return render(request,'org-detail-homepage.html',{
            'all_teachers':all_teachers,
            'all_courses':all_courses,
            'course_org':course_org,
            'current_page':current_page,
            'has_fav':has_fav,
        })

class OrgCourseView(View):
    '''
    机构课程列表页面
    '''
    def get(self,request,org_id):
        # 取出对应的课程机构
        course_org = CourseOrg.objects.get(id=int(org_id))

        # 根据外键取出所有的课程
        all_courses = course_org.course_set.all()

        # 收藏功能判断用户是否登陆
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True

        # 这个值用于org_base.html页面的选中做铺垫
        current_page = 'course'
        return render(request,'org-detail-course.html',{
            'all_courses':all_courses,
            'course_org':course_org,
            'current_page': current_page,
            'has_fav':has_fav,
        })


class OrgDescView(View):
    '''
    机构课程列表页面
    '''
    def get(self,request,org_id):
        # 取出对应的课程机构
        course_org = CourseOrg.objects.get(id=int(org_id))

        # 收藏功能判断用户是否登陆
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True

        # 这个值用于org_base.html页面的选中做铺垫
        current_page = 'desc'
        return render(request,'org-detail-desc.html',{
            'course_org':course_org,
            'current_page': current_page,
            'has_fav':has_fav,
        })


class OrgTeacherView(View):
    '''
    机构教师
    '''
    def get(self,request,org_id):
        # 取出对应的课程机构
        course_org = CourseOrg.objects.get(id=int(org_id))

        # 根据外键取出所有教师
        all_teachers = course_org.teacher_set.all()

        # 收藏功能判断用户是否登陆
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True

        # 这个值用于org_base.html页面的选中做铺垫
        current_page = 'teacher'
        return render(request,'org-detail-teachers.html',{
            'course_org':course_org,
            'all_teachers':all_teachers,
            'current_page': current_page,
            'has_fav':has_fav
        })

class AddFavView(View):
    '''
    用户收藏,用户取消收藏. 前端AJAX提交post请求
    '''
    def post(self,request):
        fav_id = request.POST.get('fav_id',0)
        fav_type = request.POST.get('fav_type',0)

        # 首先要判断用户是否登陆
        if not request.user.is_authenticated():
            return HttpResponse(json.dumps({'status': 'fail','msg':'用户未登录'}), content_type='application/json')

        # 查找已存在的记录
        exist_record = UserFavorite.objects.filter(user=request.user,fav_id=int(fav_id),fav_type=int(fav_type))
        if exist_record:
            # 如果记录已经存在，则表示用户取消收藏
            UserFavorite.objects.filter(user=request.user,fav_id=int(fav_id),fav_type=int(fav_type)).delete()
            return HttpResponse(json.dumps({'status': 'success', 'msg': '收藏'}), content_type='application/json')

        else:
            user_fav = UserFavorite()
            if int(fav_id) > 0 and int(fav_type) >0:
                user_fav.user = request.user
                user_fav.fav_id = int(fav_id)
                user_fav.fav_type = int(fav_type)
                user_fav.save()
                return HttpResponse(json.dumps({'status': 'success', 'msg': '已收藏'}), content_type='application/json')

            else:
                return HttpResponse(json.dumps({'status': 'fail', 'msg': '收藏出错'}), content_type='application/json')



class TeacherView(View):
    def get(self,request):
        all_teachers = Teacher.objects.all()

        # 首页全局导航栏中的关键词字段(课程搜索)
        search_keywords = request.GET.get('keywords', '')
        if search_keywords:
            # 对关键词字段进行数据库like查找匹配
            all_teachers = all_teachers.filter(
                Q(work_company__icontains=search_keywords) | Q(name__icontains=search_keywords)|Q(work_position__icontains=search_keywords))

        # 根据人气对讲师进行排序
        sort = request.GET.get('sort','')
        if sort:
            if sort == 'hot':
                all_teachers = all_teachers.order_by("-click_num")


         # 页面右边的讲师排行榜
        sorted_teachers = Teacher.objects.all().order_by('-click_num')[:3]



        # 对机构教师进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        # 为Paginator提供完整查询字符串生成的请求对象
        p = Paginator(all_teachers, 3, request=request)
        teachers = p.page(page)

        # QuerySet类型可以直接用count()统计数量
        teacher_nums = all_teachers.count()
        return render(request,'teachers-list.html',{
            'all_teachers':teachers,
            'current':'teacher',
            'sort':sort,
            'sorted_teachers':sorted_teachers
        })


class TeacherDetailView(View):
    def get(self,request,teacher_id):

        teacher = Teacher.objects.filter(id=int(teacher_id)).first()

        all_course = Course.objects.filter(teacher=teacher)

        had_fav_teacher = False
        has_fav_org = False

        if UserFavorite.objects.filter(user=request.user,fav_id=teacher_id,fav_type=3):
            had_fav_teacher = True
        if UserFavorite.objects.filter(user=request.user,fav_id=teacher.org.id,fav_type=2):
            has_fav_org = True

        # 页面右边的讲师排行榜
        sorted_teachers = Teacher.objects.all().order_by('-click_num')[:3]

        return render(request,'teacher-detail.html',{
            'teacher':teacher,
            'all_course':all_course,
            'sorted_teachers': sorted_teachers,
            'had_fav_teacher':had_fav_teacher,
            'had_fav_org':has_fav_org,
            'current':'teacher'
        })