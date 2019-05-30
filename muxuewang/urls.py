"""muxuewang URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import TemplateView
import xadmin
from django.views.static import serve   # 导入相关静态文件处理的views控制包
from muxuewang.settings import MEDIA_ROOT

from users import urls
from users.views import LoginView, LogoutView, RegisterView, AciveUserView, ForgetPwdView, ResetView, ModifyPwdView
from users.views import IndexView
from users.views import UserinfoView
from organization.views import OrgView

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('xadmin/',xadmin.site.urls),
    path('', IndexView.as_view(), name="index"),    #  继承TemplateView 视图类功能
    path('login.html/', LoginView.as_view(), name="login"),
    path('logout.html/', LogoutView.as_view(), name="logout"),
    path('register.html/', RegisterView.as_view(), name="register" ),
    path('captcha/', include('captcha.urls')),
    re_path(r'^active/(?P<active_code>.*)/$',AciveUserView.as_view(), name="user_active"),
    path('forgetpwd/', ForgetPwdView.as_view(), name="forget_pwd"),
    re_path(r'^reset/(?P<active_code>.*)/$',ResetView.as_view(), name="reset_pwd"),
    path('modify_pwd/', ModifyPwdView.as_view(), name="modify_pwd"),

    # 课程机构url配置
    path('org/', include('organization.urls',namespace="org")),

    # 课程url配置
    path('course/', include('courses.urls',namespace="course")),

    # 配置上传文件的访问处理函数
    re_path(r'^media/(?P<path>.*)$', serve, {"document_root": MEDIA_ROOT}),

    # re_path(r'^static/(?P<path>.*)$', serve, {"document_root": STATIC_ROOT}),

    # 课程相关url配置
    path('users/', include('users.urls', namespace='users'))

]

# 全局404 500页面配置
handler404 = 'users.views.page_not_found'
handler500 = 'users.views.page_error'