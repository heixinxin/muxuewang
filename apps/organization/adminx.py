__author__ = '星空大师'
__date__ = '2019/3/7 0007 21:13'

import xadmin
from .models import CityDict, CourseOrg, Teacher

class CityDictAdmin(object):
    list_display = ['name', 'desc', 'add_time']
    search_fields = ['name', 'desc']
    list_filter = ['name', 'desc', 'add_time']

class CourseOrgAdmin(object):
    list_display = ['name', 'desc', 'click_nums','fav_nums','image','address','city','add_time']
    search_fields = ['name', 'desc', 'click_nums','fav_nums','image','address','city']
    list_filter = ['name', 'desc', 'click_nums','fav_nums','image','address','city','add_time']
    # 外键的字段 通过ajax搜索方式
    relfield_style = 'fk-ajax'

class TeacherAdmin(object):
    list_display = ['name', 'work_years', 'work_company', 'work_position', 'points', 'click_nums', 'fav_nums', 'age', 'image', 'add_time']
    search_fields = ['name', 'work_years', 'work_company', 'work_position', 'points', 'click_nums', 'fav_nums', 'age', 'image']
    list_filter = ['name', 'work_years', 'work_company', 'work_position', 'points', 'click_nums', 'fav_nums', 'age', 'image', 'add_time']

xadmin.site.register(CityDict, CityDictAdmin)
xadmin.site.register(CourseOrg, CourseOrgAdmin)
xadmin.site.register(Teacher, TeacherAdmin)