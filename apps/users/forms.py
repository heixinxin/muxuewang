__author__ = '星空大师'
__date__ = '2019/3/8 0008 19:50'

from django import forms
from captcha.fields import CaptchaField
from .models import UserProfile

class LoginForm(forms.Form):
   username = forms.CharField(required=True)
   password = forms.CharField(required=True, min_length=6)

# 验证码  form验证
class RegisterForm(forms.Form):
   email = forms.EmailField(required=True)
   password = forms.CharField(required=True, min_length=6)
   captcha =CaptchaField(error_messages={"invalid":u"验证码输入错误"})# 自定义异常  变成中文


# 找回密码的验证
class ForgetForm(forms.Form):
   email = forms.EmailField(required=True)
   captcha = CaptchaField(error_messages={"invalid":u"验证码输入错误"})

# 修改密码验证
class ModifyPwdForm(forms.Form):
   password1 = forms.CharField(required=True, min_length=6)
   password2 = forms.CharField(required=True, min_length=6)


# 修改图片 验证 直接通过上传的路径
class UploadImageForm(forms.ModelForm):
   class Meta:
      model = UserProfile
      fields = ['image']


# 用户修改基本信息 form验证
class UserInfoForm(forms.ModelForm):
   class Meta:
      model = UserProfile
      fields = ['nick_name', 'gender', 'birday', 'address', 'mobile']