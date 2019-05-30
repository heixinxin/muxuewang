from django.db import models
from datetime import datetime

from django.contrib.auth.models import AbstractUser
# Create your models here.

#  用来记录用户相关资料的表
class UserProfile(AbstractUser):
    nick_name = models.CharField(max_length=50,verbose_name=u"昵称",default=u"")
    birday = models.DateField(verbose_name=u"生日",null=True,blank=True) # 日期型和数字型不能接受空字符串  想要为空的话  要同时设置null=True  blank=True
    gender = models.CharField(max_length=10,choices=(("male",u"男"),("female",u"女")),default="female") # choices 是django处理一些下拉框或单多选框 用的
    address = models.CharField(max_length=100,default=u"")    # 地址
    mobile = models.CharField(max_length=11,null=True,blank=True) # 手机号码
    image = models.ImageField(max_length=100,upload_to="image/%Y/%m/%d/",default=u"image/default.png")# upload_to 是处理用户上传文件 的路径  上传头像保存到用时间（/%Y/%m/%d/）格式的路径避免重名

    class Meta:  #  表名   方便你在数据库导出的时候 显示他的名字 作用
        verbose_name = "用户信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username

    def unread_nums(self):
        # 获取用户未读消息的数量
        from operation.models import UserMessage
        return UserMessage.objects.filter(user=self.id, has_read=False).count()


#  邮箱验证码表
class EmailVerifyRecord(models.Model):
    code = models.CharField(max_length=20,verbose_name=u"验证码")
    email = models.EmailField(max_length=50,verbose_name=u"邮箱")
    send_type = models.CharField(verbose_name=u'验证码类型',max_length=30,choices=(("register",u"注册"),("forget",u"找回密码"),("update_email",u"修改邮箱")))
    send_time = models.DateTimeField(verbose_name=u'发送时间', default=datetime.now)  # 发送验证码的时间

    class Meta:
        verbose_name = u"邮箱验证码"
        verbose_name_plural = verbose_name

    def __str__(self):
        return '{}({})'.format(self.code,self.email)


#  轮播图表  方便上传更换 显示的图片
class Banner(models.Model):
    title = models.CharField(max_length=100,verbose_name=u"标题")
    image = models.ImageField(upload_to="banner/%Y/%m/%d/",verbose_name=u"轮播图",max_length=100)
    url = models.URLField(max_length=200,verbose_name=u"访问地址")
    index = models.IntegerField(default=100,verbose_name=u"顺序") # 这里是决定 轮播图播放的顺序， 值改小就在前面 大就在后面
    add_time = models.DateTimeField(default=datetime.now,verbose_name=u"添加时间") # 该条记录发生的时间

    class Meta:
        verbose_name = u"轮播图"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title
