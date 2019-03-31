from django.shortcuts import render
from django.views.generic import View
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
# Create your views here.

from .models import CourseOrg,CityDict
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