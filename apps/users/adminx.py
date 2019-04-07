# _*_ coding: utf-8 _*_
__author__ = 'rapzhang'
__date__ = '2019/3/2 10:34'

import xadmin
# 全局配置必须导入views
from xadmin import views


from .models import EmailVerifyRecord,Banner

# 主题选项设置
class BaseSetting(object):
    # 使用主题功能
    enable_themes = True
    use_bootswatch = True


# 针对所有的样式的修改设置
class GlobalSettings(object):
    # 页面左上角信息
    site_title = '奔哥管理后台系统'
    site_footer = 'Rapzhang的在线教育平台'
    menu_style = 'accordion'




# 新建model的管理类
class EmailVerifyRecordAdmin(object):
    # 显示字段
    list_display = ['code','email','send_type','send_time']

    # 搜索的字段,一般不加如时间的字段
    search_fields = ['code','email','send_type']

    # 过滤器功能(强大)
    list_filter = ['code','email','send_type','send_time']
    model_icon = 'fa fa-envelope'

class BannerAdmin(object):
    list_display = ['title','image','url','index','add_time']
    search_fields = ['title','image','url','index']
    list_filter = ['title','image','url','index','add_time']


# 注册同步到xadmin管理后台页面
xadmin.site.register(EmailVerifyRecord,EmailVerifyRecordAdmin)
xadmin.site.register(Banner,BannerAdmin)
xadmin.site.register(views.BaseAdminView,BaseSetting)
xadmin.site.register(views.CommAdminView,GlobalSettings)

