__author__ = '星空大师'
__date__ = '2019/3/7 0007 20:55'

from .models import Course, Lesson, Video, CourseResource, BannerCourse
import xadmin
from organization.models import CourseOrg

# 把章节放到课程里面编辑
class LessonInline(object):
    model = Lesson
    extra = 0


class CourseResourceInline(object):
    model = CourseResource
    extra = 0

class CourseAdmin(object):
    list_display = ['name','desc','degree','learn_times','students','fav_nums','click_nums','add_time', 'get_zj_nums', 'go_to']
    search_fields = ['name','desc','degree','learn_times','students','fav_nums','click_nums']
    list_filter = ['name','desc','degree','learn_times','students','fav_nums','click_nums','add_time']
    # 对该字段排序
    ordering = ['-click_nums']
    # 禁止对改字段修改功能
    readonly_fields = ['click_nums']
    # 直接可以在外面显示的位置修改
    list_editable = ['degree', 'desc']
    # 隐藏此字段
    exclude = ['fav_nums']
    style_fields = {"detail":"ueditor"}
    # 添加到一张表里面编辑的 关键词
    inlines = [LessonInline, CourseResourceInline]


    def queryset(self):
        qs = super(CourseAdmin, self).queryset()
        qs = qs.filter(is_banner=False)
        return qs

    def save_models(self):
        # 在保存课程的时候统计课程机构的课程数
        obj = self.new_obj
        obj.save()
        if obj.course_org is not None:
            # 如果这个课程有机构 先查出这个机构
            course_org = obj.course_org
            course_org.course_nums = Course.objects.filter(course_org=course_org).count()

            course_org.save()

class BannerCourseAdmin(object):
    list_display = ['name', 'desc', 'degree', 'learn_times', 'students', 'fav_nums', 'click_nums', 'add_time', 'get_zj_nums', 'go_to']
    search_fields = ['name', 'desc', 'degree', 'learn_times', 'students', 'fav_nums', 'click_nums']
    list_filter = ['name', 'desc', 'degree', 'learn_times', 'students', 'fav_nums', 'click_nums', 'add_time']
    # 对该字段排序
    ordering = ['-click_nums']
    # 禁止对改字段修改功能
    readonly_fields = ['click_nums']
    # 隐藏此字段
    exclude = ['fav_nums']
    # 添加到一张表里面编辑的 关键词
    inlines = [LessonInline, CourseResourceInline]

    def queryset(self):
        # queryset是查询集  就是传到服务器上的url里面的查询内容。 django会对查询返回的结果集QuerySet进行缓存
        qs = super(BannerCourseAdmin, self).queryset()
        qs = qs.filter(is_banner=True)
        return qs


class LessonAdmin(object):
    list_display = ['course','name','add_time']
    search_fields = ['course','name']
    list_filter = ['course__name','name','add_time']

class VideoAdmin(object):
    list_display = ['lesson','name','add_time']
    search_fields = ['lesson','name']
    list_filter = ['lesson','name','add_time']

class CourseResourceAdmin(object):
    list_display = ['course','name','download','add_time']
    search_fields = ['course','name','download']
    list_filter = ['course','name','download','add_time']

xadmin.site.register(Course, CourseAdmin)
xadmin.site.register(BannerCourse, BannerCourseAdmin)
xadmin.site.register(Lesson, LessonAdmin)
xadmin.site.register(Video, VideoAdmin)
xadmin.site.register(CourseResource, CourseResourceAdmin)