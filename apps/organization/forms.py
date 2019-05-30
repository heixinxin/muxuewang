__author__ = '星空大师'
__date__ = '2019/3/11 0011 17:23'

from django import forms
import re
from operation.models import UserAsl

class UserAskForm(forms.ModelForm):

    class Meta:
        model = UserAsl
        fields = ['name','mobile', 'course_name']      #  把需要验证的字段放进这里面

    def clean_mobile(self):
        '''
        验证手机号码是否合法
        :return:
        '''
        mobile = self.cleaned_data["mobile"]   # 取出用户输入的电话号码
        REGEX_MOBILE = "^1[358]\d{9}$|^147\d{8}$|^176\d{8}$"
        p = re.compile(REGEX_MOBILE)
        print(p.match(mobile))
        if p.match(mobile):
            return mobile
        else:
            raise forms.ValidationError(u"手机号码非法", code="mobile_invalid")