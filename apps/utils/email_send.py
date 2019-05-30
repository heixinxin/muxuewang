__author__ = '星空大师'
__date__ = '2019/3/9 0009 16:41'

from random import Random
from django.core.mail import send_mail  # 用来发邮件

from users.models import EmailVerifyRecord
from muxuewang.settings import EMAIL_FROM


def random_str(randomlength=8):
    str = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'   # 让我们的验证码从这些字符串中 随机选几个
    length = len(chars) - 1
    random = Random()
    for i in range(randomlength):
        str+=chars[random.randint(0, length)]   # 随机选一个数  字符串进行拼接
    return str

#  邮箱发送代码
def send_register_email(email,send_type="register"):
    email_record = EmailVerifyRecord()
    if send_type == "update_email":
        code = random_str(4)
    else:
        code = random_str(8)
    email_record.code = code
    email_record.email = email
    email_record.send_type = send_type
    email_record.save()

    email_title = ""
    email_body = ""

    if send_type == "register":
        email_title = "点灯人在线网注册激活链接"
        email_body = "请点击下面的链接激活你的账号: http://127.0.0.1:8000/active/{0}".format(code)

        # 发送邮件得到一个真假 值
        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])


        if send_status:
            pass

    elif send_type == "forget":
        email_title = "点灯人在线网修改密码重置链接"
        email_body = "请点击下面的链接重置密码: http://127.0.0.1:8000/reset/{0}".format(code)

        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])

        if send_status:
            pass

    elif send_type == "update_email":
        email_title = "点灯人在线邮箱修改验证码"
        email_body = "你的邮箱验证码为: {0}".format(code)

        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])

        if send_status:
            pass