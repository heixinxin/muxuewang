from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.base import View
from .models import Course, CourseResource
from django.db.models import Q
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger  # 分页模块功能的导入
from operation.models import UserFavorite, CourseComments, UserCourse
from utils.mixin_utils import LoginRequiredMixin
# Create your views here.


class CourseListView(View):
    def get(self, request):
        all_courses = Course.objects.all().order_by("-add_time")
        hot_courses = Course.objects.all().order_by("-click_nums")[:3]

        # 课程搜索
        search_keywords = request.GET.get("keywords", '')
        if search_keywords:
            all_courses = all_courses.filter(Q(name__icontains=search_keywords)|Q(desc__icontains=search_keywords)|Q(detail__icontains=search_keywords))

        # 课程排序
        sort = request.GET.get('sort', '')
        if sort:
            if sort == "students":
                all_courses = all_courses.order_by("-students")
            elif sort == "hot":
                all_courses = all_courses.order_by("-click_nums")


        # 对课程机构进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_courses, 6, request=request)  # 对几条数据一页

        courses = p.page(page)

        return render(request, 'course-list.html', {
            'courses':courses,
            'sort':sort,
            'hot_courses':hot_courses
        })

# 课程详情页
class CourseDetailView(View):
    '''
    课程详情页
    '''
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))

        # 增加课程点击数
        course.click_nums += 1
        course.save()

        # 是否收藏课程
        has_fav_course = False
        # 是否收藏机构
        has_fav_org = False

        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course.id, fav_type=1):
                has_fav_course = True

            if UserFavorite.objects.filter(user=request.user, fav_id=course.course_org.id, fav_type=2):
                has_fav_org = True

        # 筛选出推荐的课程
        tag = course.tag
        if tag:
            relate_coures = Course.objects.filter(tag=tag)[:1]
        else:
            relate_coures = []

        return render(request, 'course-detail.html', {
            'course':course,
            'relate_coures':relate_coures,
            'has_fav_course':has_fav_course,
            'has_fav_org':has_fav_org
        })

# 课程章节信息
class CourseInfoView(LoginRequiredMixin, View):
    '''
    课程章节信息
    '''
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        course.students += 1
        course.save()
        # 查询用户是否已经关联了该课程   点击开始学习没有关联的就关联
        user_cousers = UserCourse.objects.filter(user=request.user, course=course)
        if not user_cousers:
            user_couser = UserCourse(user=request.user, course=course)  # 把用户和课程id给存进去
            user_couser.save()

        user_cousers = UserCourse.objects.filter(course=course)  # 取出这门课程的所有对应的用户
        user_ids = [user_couser.user.id for user_couser in user_cousers]  # 取出所有用户的id
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids) # 用_in 返回一列表 所有用户信息
        # 取出所有课程id
        course_ids = [user_couser.course.id for user_couser in all_user_courses]
        # 获取学过该用户学过其他的所有课程
        relate_courses = Course.objects.filter(id__in=course_ids).order_by('-click_nums')[:5]
        all_resources = CourseResource.objects.filter(course=course)
        return render(request, 'course-video.html', {
            "course":course,
            'course_resources':all_resources,
            'relate_courses':relate_courses
        })


class CommentView(LoginRequiredMixin, View):
    '''
    课程评论
    '''
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))

        all_resources = CourseResource.objects.filter(course=course)
        all_comment = CourseComments.objects.filter(course_id=course_id).order_by('-id')
        return render(request, 'course-comment.html', {
            "course":course,
            'course_resources':all_resources,
            'all_comment':all_comment
        })


class AddComentsView(View):
    '''
    用户添加课程评论
    '''

    def post(self, request):
        if not request.user.is_authenticated:
            # 判断用户登录状态
            return HttpResponse('{"status":"fail", "msg":"用户未登录"}', content_type='application/json')

        course_id = request.POST.get("course_id", 0)
        comments = request.POST.get('comments', '')
        if int(course_id) > 0 and comments:   # 传过来的课程course_id必须是大于1的
            course_comments = CourseComments()
            course = Course.objects.get(id=int(course_id))  # 筛选评论的课程
            course_comments.course = course
            course_comments.comments = comments
            course_comments.user = request.user
            course_comments.save()
            return HttpResponse('{"status":"success", "msg":"添加成功"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail", "msg":"添加失败"}', content_type='application/json')


