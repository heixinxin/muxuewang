__author__ = '星空大师'
__date__ = '2019/3/14 0014 13:41'



# 主要实现 用户点击开始学习 判断用户是否登录
# 用mixin装饰器来检测用户是否登录
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

class LoginRequiredMixin(object):

    @method_decorator(login_required(login_url='/login.html/', redirect_field_name=None))
    def dispatch(self, request, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(request, *args, **kwargs)