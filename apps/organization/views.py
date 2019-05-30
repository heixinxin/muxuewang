from django.shortcuts import render

# Create your views here.
from django.views import View
from .forms import UserAskForm
from operation.models import UserFavorite
from organization.models import CourseOrg, CityDict
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger  # 分页模块功能的导入
from django.http import HttpResponse
from .models import Teacher
from django.db.models import Q
from courses.models import Course


# 课程机构列表功能
class OrgView(View):
    """
    课程机构列表功能
    """
    def get(self,request):
        # 课程机构
        all_orgs = CourseOrg.objects.all()
        hot_orgs = all_orgs.order_by("-click_nums")[0:3]   #  order_by是django中一个排序函数

        # 城市
        all_citys = CityDict.objects.all()


        # 机构导航栏的搜索   有前端js加入参数
        search_keywords = request.GET.get("keywords", "")
        if search_keywords:
            all_orgs = all_orgs.filter(Q(name__icontains=search_keywords)|Q(desc__icontains=search_keywords)) # __相当于模糊查询


        # 取出筛选城市
        city_id = request.GET.get('city', '')
        if city_id:
            all_orgs = all_orgs.filter(city_id=int(city_id))   # 用前端传过来的城市id 在课程机构表中找


        # 取出筛选机构类别
        category = request.GET.get('ct', '')
        if category:
            all_orgs = all_orgs.filter(category=category)  # 用前端传过来的机构名称 在课程机构表中找

        # 课程机构排序
        sort = request.GET.get('sort', '')
        if sort:
            if sort == "students":
                all_orgs = all_orgs.order_by("-students")
            elif sort == "courses":
                all_orgs = all_orgs.order_by("-course_nums")



        # 统计有多少个
        org_nums = all_orgs.count()



        # 对课程机构进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_orgs, 5, request=request)  # 对几条数据一页

        # 统计有多少个
        orgs = p.page(page)


        return render(request, 'org-list.html', {
            "all_orgs":orgs,
            "all_citys":all_citys,
            "org_nums":org_nums,
            "city_id":city_id,
            "category":category,
            'hot_orgs':hot_orgs,
            'sort':sort
        })

# 用户添加咨询
class AddUserAskView(View):
    """
    用户添加咨询
    """
    def post(self, request):
        userask_form = UserAskForm(request.POST)
        if userask_form.is_valid():
            user_ask = userask_form.save(commit=True)    # 用formModel可以直接保存  不用在实例化 赋值在保存
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail", "msg":"添加出错"}', content_type='application/json')


# 机构首页
class OrgHomeView(View):
    '''
    机构首页
    '''
    def get(self, request, org_id):
        current_page = "home"
        course_org = CourseOrg.objects.get(id=int(org_id))   #  所有机构匹配点击的是谁， 通过url传过来的id查找
        # 点开课程机构 就 +1
        course_org.click_nums += 1
        course_org.save()
        has_fav = False
        if request.user.is_authenticated:  # 检测用户是否登录
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):  # 如果数据库里有这条收藏记录
                has_fav = True
        all_courses = course_org.course_set.all()[:3]       #  取出外键 的所有课程
        all_teachers = course_org.teacher_set.all()[:1]    # 取出外键 的所有老师
        return  render(request, 'org-detail-homepage.html', {
            'all_courses':all_courses,
            'all_teachers':all_teachers,
            'course_org':course_org,
            'current_page':current_page,
            'has_fav':has_fav
        })


# 机构课程列表页
class OrgCourseView(View):
    '''
    机构课程列表页
    '''
    def get(self, request, org_id):
        current_page = "course"
        course_org = CourseOrg.objects.get(id=int(org_id))   #  所有机构匹配点击的是谁， 通过url传过来的id查找
        has_fav = False
        if request.user.is_authenticated:  # 检测用户是否登录
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):  # 如果数据库里有这条收藏记录
                has_fav = True
        all_courses = course_org.course_set.all()[:3]            #  取出外键 的所有课程
        return  render(request, 'org-detail-course.html', {
            'all_courses':all_courses,
            'course_org':course_org,
            'current_page':current_page,
            'has_fav':has_fav
        })


# 机构介绍
class OrgDescView(View):
    '''
    机构介绍页
    '''
    def get(self, request, org_id):
        current_page = "desc"
        course_org = CourseOrg.objects.get(id=int(org_id))   #  所有机构匹配点击的是谁， 通过url传过来的id查找
        has_fav = False
        if request.user.is_authenticated:  # 检测用户是否登录
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):  # 如果数据库里有这条收藏记录
                has_fav = True
        return  render(request, 'org-detail-desc.html', {
            'course_org':course_org,
            'current_page':current_page,
            'has_fav':has_fav
        })

# 机构教师
class OrgTeachersView(View):
    '''
    机构教师页
    '''
    def get(self, request, org_id):
        current_page = "teachers"
        course_org = CourseOrg.objects.get(id=int(org_id))   #  所有机构匹配点击的是谁， 通过url传过来的id查找
        has_fav = False
        if request.user.is_authenticated:  # 检测用户是否登录
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):  # 如果数据库里有这条收藏记录
                has_fav = True
        all_teachers = course_org.teacher_set.all()[:1]    # 取出外键 的所有老师
        return  render(request, 'org-detail-teachers.html', {
            'all_teachers':all_teachers,
            'course_org':course_org,
            'current_page':current_page,
            'has_fav':has_fav
        })


# 用户收藏
class AddFavView(View):
    '''
    用户收藏， 用户取消收藏
    '''
    def post(self, request):
        fav_id = request.POST.get('fav_id', 0)
        fav_type = request.POST.get('fav_type', 0)

        if not request.user.is_authenticated:   #  is_authenticated判断用户登录的函数
            # 判断用户登录状态
            return HttpResponse('{"status":"fail", "msg":"用户未登录"}', content_type='application/json')

        exist_records = UserFavorite.objects.filter(user=request.user, fav_id=int(fav_id), fav_type=int(fav_type))
        if exist_records:
            # 如果记录已经存在， 则表示用户取消收藏
            exist_records.delete()
            # 存储收藏数
            if int(fav_type) == 1:
                course = Course.objects.get(id=int(fav_id))
                course.fav_nums -= 1
                # 收藏数小于0 就等于0 避免负数
                if course.fav_nums <0:
                    course.fav_nums = 0
                course.save()
            elif int(fav_type) == 2:
                course_org = CourseOrg.objects.get(id=int(fav_id))
                course_org.fav_nums -= 1
                if course_org.fav_nums <0:
                    course_org.fav_nums = 0
                course_org.save()
            elif int(fav_type) == 3:
                teacher = Teacher.objects.get(id=int(fav_id))
                teacher.fav_nums -= 1
                if teacher.fav_nums < 0:
                    teacher.fav_nums = 0
                teacher.save()

            return HttpResponse('{"status":"success", "msg":"收藏"}', content_type='application/json')
        else:
            # 如果记录不存在  就收藏
            user_fav = UserFavorite()
            if int(fav_type) > 0 and int(fav_id) > 0:
                user_fav.user = request.user
                user_fav.fav_id = int(fav_id)
                user_fav.fav_type = int(fav_type)
                user_fav.save()

                # 各收藏数 +1
                if int(fav_type) == 1:
                    course = Course.objects.get(id=int(fav_id))
                    course.fav_nums += 1
                    course.save()
                elif int(fav_type) == 2:
                    course_org = CourseOrg.objects.get(id=int(fav_id))
                    course_org.fav_nums += 1
                    course_org.save()
                elif int(fav_type) == 3:
                    teacher = Teacher.objects.get(id=int(fav_id))
                    teacher.fav_nums += 1
                    teacher.save()

                return HttpResponse('{"status":"success", "msg":"已收藏"}', content_type='application/json')
            else:
                return HttpResponse('{"status":"fail", "msg":"收藏出错"}', content_type='application/json')


# 课程讲师列表页
class TeacherListView(View):
    '''
    课程讲师列表页
    '''
    def get(self, request):
        all_teachers = Teacher.objects.all()

        # 课程讲师导航栏的搜索   有前端js加入参数
        search_keywords = request.GET.get("keywords", "")
        if search_keywords:
            all_teachers = all_teachers.filter(Q(name__icontains=search_keywords)|
                                               Q(work_company__icontains=search_keywords)|
                                               Q(work_position__icontains=search_keywords))  # __相当于模糊查询

        sort = request.GET.get('sort', "")
        if sort:
            if sort == "hot":
                all_teachers = all_teachers.order_by("-click_nums")

        sorted_teacher = Teacher.objects.all().order_by("-click_nums")[:3]



        # 统计有多少个
        org_nums = all_teachers.count()

        # 对讲师进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_teachers, 5, request=request)  # 对几条数据一页

        # 统计有多少个
        teachers = p.page(page)

        return render(request, 'teachers-list.html', {
            'all_teachers':teachers,
            'sorted_teacher':sorted_teacher,
            'sort':sort,
            'org_nums':org_nums
        })


# 讲师详情
class TeacherDetailView(View):
    '''
    讲师详情
    '''
    def get(self, request, teacher_id):
        teacher = Teacher.objects.get(id=int(teacher_id))
        # 点击老师进入页面就 + 1
        teacher.click_nums += 1
        teacher.save()

        all_courses = Course.objects.filter(teacher=teacher)


        has_teacher_faved = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_type=3, fav_id=teacher.id):
                has_teacher_faved = True

        # 判断用户收藏没有
        has_org_faved = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_type=2, fav_id=teacher.org.id):
                has_org_faved = True



        sorted_teacher = Teacher.objects.all().order_by("-click_nums")[:3]


        return render(request, 'teacher-detail.html',{
            'teacher':teacher,
            'all_courses':all_courses,
            'sorted_teacher':sorted_teacher,
            'has_teacher_faved':has_teacher_faved,
            'has_org_faved':has_org_faved
        })