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
        # QuerySet类型可以直接用count()统计数量
        org_nums = all_orgs.count()
        all_citys = CityDict.objects.all()

        # 对课程机构进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        # 为Paginator提供完整查询字符串生成的请求对象
        p = Paginator(all_orgs,4,request=request)
        orgs = p.page(page)

        return render(request,'org-list.html',{
            'all_orgs':orgs,
            'all_citys':all_citys,
            'org_nums':org_nums
        })