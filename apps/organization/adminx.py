# _*_ coding: utf-8 _*_
__author__ = 'rapzhang'
__date__ = '2019/3/2 13:25'

import xadmin
from .models import CourseOrg,CityDict,Teacher

class CityDictAdmin(object):
    list_display = ['name', 'desc', 'add_time']
    search_fields = ['name', 'desc']
    list_filter = ['name', 'desc', 'add_time']


class CourseOrgAdmin(object):
    list_display = ['name', 'desc', 'click_num','fav_nums','image','address','city','add_time']
    search_fields = ['name', 'desc', 'click_num','fav_nums','image','address','city']
    list_filter = ['name', 'desc', 'click_num','fav_nums','image','address','city','add_time']


class TeacherAdmin(object):
    list_display = ['org', 'name', 'work_years','work_company','work_position','points','click_num','fav_nums','add_time']
    search_fields = ['org', 'name', 'work_years','work_company','work_position','points','click_num','fav_nums']
    list_filter = ['org', 'name', 'work_years','work_company','work_position','points','click_num','fav_nums','add_time']



xadmin.site.register(CityDict,CityDictAdmin)
xadmin.site.register(CourseOrg,CourseOrgAdmin)
xadmin.site.register(Teacher,TeacherAdmin)