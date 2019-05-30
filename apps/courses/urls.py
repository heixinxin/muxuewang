__author__ = '星空大师'
__date__ = '2019/3/11 0011 17:22'
from django.urls import path, include, re_path
from .views import CourseListView, CourseDetailView, CourseInfoView, CommentView, AddComentsView

app_name = '[course]'
urlpatterns = [
    # 课程列表页
    path('list/', CourseListView.as_view(), name="course_list"),

    # 课程详情页
    re_path(r'^detail/(?P<course_id>\d+)/$', CourseDetailView.as_view(), name="course_detail"),

    re_path(r'^info/(?P<course_id>\d+)/$', CourseInfoView.as_view(), name="course_info"),

    # 课程评论
    re_path(r'^comment/(?P<course_id>\d+)/$', CommentView.as_view(), name="course_comment"),

    path('add_comment/', AddComentsView.as_view(), name="add_comment"),

]
