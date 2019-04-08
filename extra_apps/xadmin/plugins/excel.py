# _*_ coding:utf-8 _*_
__author__ = 'rapzhang'
__data__ = '2019/4/8 11:59'


import xadmin
from xadmin.views import BaseAdminPlugin,ListAdminView
from django.template import loader

# excel导入
class ListImportExcelPlugin(BaseAdminPlugin):
    import_excel = True

    def init_request(self, *args, **kwargs):
        return bool(self.import_excel)



xadmin.site.register_plugin(ListImportExcelPlugin,ListAdminView)