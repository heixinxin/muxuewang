__author__ = '星空大师'
__date__ = '2019/3/11 0011 17:22'
from django.urls import path, include, re_path
from .views import OrgView, AddUserAskView, OrgHomeView, OrgCourseView, OrgDescView, OrgTeachersView, AddFavView
from .views import TeacherListView, TeacherDetailView

app_name = '[org]'
urlpatterns = [
    # 课程机构列表页
    path('list/', OrgView.as_view(), name="org_list"),
    path('add_ask/', AddUserAskView.as_view(), name='add_ask'),
    re_path(r'^home/(?P<org_id>\d+)/$', OrgHomeView.as_view(), name='org_home'),
    re_path(r'^course/(?P<org_id>\d+)/$', OrgCourseView.as_view(), name='org_course'),
    re_path(r'^desc/(?P<org_id>\d+)/$', OrgDescView.as_view(), name='org_desc'),
    re_path(r'^org_teachers/(?P<org_id>\d+)/$', OrgTeachersView.as_view(), name='org_teachers'),

    # 机构收藏
    path('add_fav/', AddFavView.as_view(), name='add_fav'),

    # 讲师列表页
    path('teacher/list/', TeacherListView.as_view(), name='teacher_list'),

    # 讲师详情页
    re_path(r'^teacher/detail/(?P<teacher_id>\d+)/$', TeacherDetailView.as_view(), name='teacher_detail'),

]
