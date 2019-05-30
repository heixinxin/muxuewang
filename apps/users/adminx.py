__author__ = '星空大师'
__date__ = '2019/3/7 0007 20:19'

import xadmin
from .models import EmailVerifyRecord,Banner
from xadmin import views

# 主题设置显示
class BaseSetting(object):
    enable_themes = True  #
    use_bootswatch = True  # 多种主题样式开启

# 标题 页脚的更改
class GlobalSettings(object):
    site_title = "点灯人后台管理"
    site_footer = "点灯人在线网"
    menu_style = "accordion"   # app列表收缩


class EmailVerifyRecordAdmin(object):
    list_display = ['code','email','send_type','send_time']  # 添加显示 列段
    search_fields = ['code','email','send_type']   #  添加查找功能
    list_filter = ['code','email','send_type','send_time']  # 添加过滤器功能


class BannerAdmin(object):
    list_display = ['title','image','url','index','add_time']
    search_fields = ['title','image','url','index']
    list_filter = ['title','image','url','index','add_time']

xadmin.site.register(EmailVerifyRecord, EmailVerifyRecordAdmin)  # 将模块添加到后台显示界面中
xadmin.site.register(Banner, BannerAdmin)
xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView, GlobalSettings)