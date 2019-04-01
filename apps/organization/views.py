import json

from django.shortcuts import render
from django.views.generic import View
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse,JsonResponse
# Create your views here.

from .models import CourseOrg,CityDict
from .forms import UserAskForm
from courses.models import Course


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

        # 这个值用于org_base.html页面的选中做铺垫
        current_page = 'home'
        return render(request,'org-detail-homepage.html',{
            'all_teachers':all_teachers,
            'all_courses':all_courses,
            'course_org':course_org,
            'current_page':current_page
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

        # 这个值用于org_base.html页面的选中做铺垫
        current_page = 'course'
        return render(request,'org-detail-course.html',{
            'all_courses':all_courses,
            'course_org':course_org,
            'current_page': current_page
        })


class OrgDescView(View):
    '''
    机构课程列表页面
    '''
    def get(self,request,org_id):
        # 取出对应的课程机构
        course_org = CourseOrg.objects.get(id=int(org_id))

        # 这个值用于org_base.html页面的选中做铺垫
        current_page = 'desc'
        return render(request,'org-detail-desc.html',{
            'course_org':course_org,
            'current_page': current_page
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

        # 这个值用于org_base.html页面的选中做铺垫
        current_page = 'teacher'
        return render(request,'org-detail-teachers.html',{
            'course_org':course_org,
            'all_teachers':all_teachers,
            'current_page': current_page
        })