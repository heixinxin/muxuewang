from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
# authenticate 是django内置函数 用来处理用户输入的用户名和密码是否正确  login 是django处理登陆用的
from django.contrib.auth import authenticate, login, logout
# 可以重写authenticate 方法
from django.contrib.auth.backends import ModelBackend
# 来判断输入的 账号和邮箱
from django.db.models import Q
# View里 用类的  不用 def
from django.views.generic import View
# 验证 form 表单引用
from .forms import LoginForm, RegisterForm, ForgetForm, ModifyPwdForm, UploadImageForm, UserInfoForm
# 可以将注册的明文密码转换成密文
from django.contrib.auth.hashers import make_password
from utils.mixin_utils import LoginRequiredMixin
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

from .models import UserProfile, EmailVerifyRecord, Banner
# Create your views here.
from utils.email_send import send_register_email
from operation.models import UserCourse, UserFavorite, UserMessage
from organization.models import CourseOrg, Teacher
from courses.models import Course
import json
# django2.0已经把 core换成了urls
from django.urls import reverse

# 重写authenticate方法  来检验登陆的账号和密码
class CustomBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username)|Q(email=username)) # 用Q 加| 相当于 或
            if user.check_password(password):  # 密码验证 因为django给我们存的是密文 所以要用check_password方法
                return user
        except Exception as e:
            return None

#  用户激活邮箱
class AciveUserView(View):
    def get(self, request, active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code)   # 在邮箱表 中找到这条数据
        print(all_records)
        if all_records:
            for record in all_records:
                email = record.email
                user = UserProfile.objects.get(email=email)  #  在用户表中找到这个人
                user.is_active = True
                user.save()
        else:
            return render(request, "active_fail.html")  #  链接错误  给出链接失效页面
        return render(request, "login.html")    #  激活成功页面

#  注册账号函数
class RegisterView(View):
    def get(self, request):
        register_form = RegisterForm()  # 验证码 实例化
        return render(request, "register.html", {'register_form':register_form})

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user_name = request.POST.get("email", "")
            if UserProfile.objects.filter(email=user_name):  #  判断用户是否在 数据库中
                return render(request, "register.html", {"register_form":register_form, "msg":"用户已经存在"})
            pass_word = request.POST.get("password", "")
            user_profile = UserProfile()
            user_profile.username = user_name
            user_profile.email = user_name
            user_profile.is_active = False
            user_profile.password = make_password(pass_word)  #  转换成密文
            user_profile.save()

            # 写入欢迎组注册消息
            user_message = UserMessage()
            user_message.user = user_profile.id
            user_message.message = '欢迎注册星空在线网'
            user_message.save()

            send_register_email(user_name, "register")
            return render(request, "login.html")
        else:
            msg = ""
            if request.POST.get("password", "") == "":
                msg = "密码不能为空"
            return render(request, "register.html", {"register_form":register_form, "msg":msg})


# 用户退出
class LogoutView(View):
    '''
    用户退出
    '''
    def get(self, request):
        # 与login函数对应的退出函数
        logout(request)

        # 定向返回  不然html路径返回不了
        return HttpResponseRedirect(reverse("index"))

# 登陆函数
class LoginView(View):
    def get(self, request):
        return render(request, "login.html", {})
    def post(self, request):
        login_form = LoginForm(request.POST)  # 传入一个字典
        if login_form.is_valid():     #  判断是否有错  验证字段 的正确性
            user_name = request.POST.get("username", "")
            pass_word = request.POST.get("password", "")
            user = authenticate(username=user_name, password=pass_word)  # 密码不合法返回 None
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(reverse("index"))
                else:
                    return render(request, "login.html", {"msg": "用户未激活"})
            else:
                return render(request, "login.html", {"msg": "用户名或密码错误"})
        else:
            return render(request, "login.html", {"login_form":login_form})

# 找回密码账号的界面
class ForgetPwdView(View):
    def get(self, request):
        forget_form = ForgetForm()
        return render(request, "forgetpwd.html", {"forget_form": forget_form})

    def post(self, request):
        forget_form = ForgetForm(request.POST)
        if forget_form.is_valid():
            email = request.POST.get("email", "")
            send_register_email(email , "forget")
            return render(request, "send_success.html")
        else:
            return render(request, "forgetpwd.html", {"forget_form":forget_form})


# 修改用户密码 get 请求验证链接
class ResetView(View):
    def get(self, request, active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        #  判断有验证码就肯定会在数据库中取出数据
        if all_records:
            for record in all_records:
                email = record.email
                return render(request, "password_reset.html", {"email":email})
        else:
            return render(request, "active_fail.html")

# 修改用户密码
class ModifyPwdView(View):
    """
    修改用户密码
    """
    def post(self, request):
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            pwd1 = request.POST.get("password1", "")
            pwd2 = request.POST.get("password2", "")
            email = request.POST.get("email", "")
            if pwd1 != pwd2:
                return render(request, "password_reset.html", {"email":email, "msg":"两次输入的密码不一致"})
            user = UserProfile.objects.get(email=email)
            user.password = make_password(pwd2)
            user.save()

            return render(request, "login.html")

        else:
            email = request.POST.get("email", "")
            return render(request, "password_reset.html",{"email":email, "modify_form":modify_form})


# 用户个人信息

class UserinfoView(LoginRequiredMixin, View):
    '''
    用户个人信息

    '''
    def get(self, request):
        return render(request, 'usercenter-info.html', {})

    def post(self, request):
        user_info_form = UserInfoForm(request.POST, instance=request.user)
        if user_info_form.is_valid():
            user_info_form.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse(json.dumps(user_info_form.errors), content_type='application/json')


# 用户修改头像
class UploadImageView(LoginRequiredMixin, View):
    '''
    用户修改头像
    '''
    def post(self, request):
        # 因为是路径 所以要导入FILES， 然后用的Modelform表单,接受instance为关键参数，  所以可以直接保存
        image_form = UploadImageForm(request.POST, request.FILES, instance=request.user)
        if image_form.is_valid():
            image_form.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail"}', content_type='application/json')


# 个人中心修改用户密码
class UpdatePwdView(LoginRequiredMixin, View):
    '''
    个人中心修改用户密码
    '''
    def post(self, request):
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            pwd1 = request.POST.get("password1", "")
            pwd2 = request.POST.get("password2", "")
            if pwd1 != pwd2:
                return HttpResponse('{"status":"fail","msg":"密码不一致"}', content_type='application/json')
            user = request.user
            user.password = make_password(pwd2)
            user.save()

            return HttpResponse('{"status":"success"}', content_type='application/json')

        else:
            return HttpResponse(json.dumps(modify_form.errors), content_type='application/json')


# 发送邮箱验证码
class SendEmailCodeView(LoginRequiredMixin, View):
    '''
    发送邮箱验证码
    '''
    def get(self, request):
        email = request.GET.get('email', '')

        # 判断该邮箱被注册 没有
        if UserProfile.objects.filter(email=email):
            return HttpResponse('{"email":"邮箱已经存在"}', content_type='application/json')
        # 传到发送邮箱的函数
        send_register_email(email, 'update_email')

        return HttpResponse('{"status":"success"}', content_type='application/json')

# 修改个人邮箱
class UpdateEmailView(LoginRequiredMixin, View):
    '''
    修改个人邮箱
    '''
    def post(self, request):
        email = request.POST.get('email', '')
        code = request.POST.get('code', '')

        existed_records = EmailVerifyRecord.objects.filter(email=email, code=code, send_type='update_email')
        # 如果有这条验证码 就更改保存
        if existed_records:
            user= request.user
            user.email = email
            user.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse('{"email":"验证码出错"}', content_type='application/json')


# 我的课程
class MyCourseView(LoginRequiredMixin, View):
    '''
    我的课程
    '''
    def get(self, request):

        rode = 'courser'
        user_courses = UserCourse.objects.filter(user=request.user)

        return render(request, 'usercenter-mycourse.html', {
            'user_courses':user_courses,
            'rode':rode
        })


# 我收藏的课程机构
class MyFavOrgView(LoginRequiredMixin, View):
    '''
    我收藏的课程机构
    '''
    def get(self, request):
        org_list = []
        rode = 'fav'
        fav_orgs = UserFavorite.objects.filter(user=request.user, fav_type=2)
        for fav_org in fav_orgs:
            # 用遍历 取出所有的课程机构id
            org_id = fav_org.fav_id
            # 取出所有的课程机构
            org = CourseOrg.objects.get(id=org_id)
            org_list.append(org)
        return render(request, 'usercenter-fav-org.html', {
            'org_list':org_list,
            'rode':rode
        })

# 我收藏的授课讲师
class MyFavTeacherView(LoginRequiredMixin, View):
    '''
    我收藏的授课讲师
    '''
    def get(self, request):
        teacher_list = []
        rode = 'fav'
        fav_teachers = UserFavorite.objects.filter(user=request.user, fav_type=3)
        for fav_teacher in fav_teachers:
            # 用遍历 取出所有的老师的id
            teacher_id = fav_teacher.fav_id
            # 取出所有的老师
            teacher = Teacher.objects.get(id=teacher_id)
            teacher_list.append(teacher)

        return render(request, 'usercenter-fav-teacher.html', {
            'teacher_list':teacher_list,
            'rode':rode
        })


# 我收藏的课程
class MyFavCourseView(LoginRequiredMixin, View):
    '''
    我收藏的课程
    '''
    def get(self, request):
        course_list = []
        rode = 'fav'
        fav_courses = UserFavorite.objects.filter(user=request.user, fav_type=1)
        for fav_course in fav_courses:
            # 用遍历 取出所有的课程的id
            course_id = fav_course.fav_id
            # 取出所有的课程
            teacher = Course.objects.get(id=course_id)
            course_list.append(teacher)
        return render(request, 'usercenter-fav-course.html', {
            'course_list':course_list,
            'rode':rode
        })


# 我的消息
class MymessageView(LoginRequiredMixin, View):
    '''
    我的消息
    '''
    def get(self, request):
        # 取出 该用户的所有消息
        all_messages = UserMessage.objects.filter(user=request.user.id)
        rode = 'messages'

        #对个人消息进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_messages, 5, request=request)

        messages = p.page(page)

        return render(request, 'usercenter-message.html', {
            'messages':messages,
            'rode':rode
        })


class ToMymessageView(LoginRequiredMixin, View):
    def get(self, request, message_id):
        message = UserMessage.objects.get(id=int(message_id))

        message.has_read = True
        message.save()
        return render(request, 'my_mymessage.html', {
            "message":message
        })


# 慕学在线网  首页
class IndexView(View):
    '''
    慕学在线网  首页
    '''
    def get(self, request):
        # 取出轮播图
        all_banners = Banner.objects.all().order_by('index')
        # 取出课程
        courses = Course.objects.filter(is_banner=False)[:6]
        # 取出三个课程出来轮播
        banner_courses = Course.objects.filter(is_banner=True)[:3]
        # 取出15个机构出来显示
        course_orgs = CourseOrg.objects.all()[:15]
        return render(request, 'index.html', {
            'all_banners':all_banners,
            'courses':courses,
            'banner_courses':banner_courses,
            'course_orgs':course_orgs
        })


# 配置404函数
def page_not_found(request):
    # 全局404处理函数
    from django.shortcuts import render_to_response
    response = render_to_response('404.html', {})
    response.status_code = 404
    return response

def page_error(request):
    # 全局500处理函数
    from django.shortcuts import render_to_response
    response = render_to_response('500.html', {})
    response.status_code = 500
    return response