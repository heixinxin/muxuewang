from django.apps import AppConfig


class CoursesConfig(AppConfig):
    name = 'courses'
    verbose_name = u"课程管理" # 将列表变成中文(不过要在__init__中添加config)
