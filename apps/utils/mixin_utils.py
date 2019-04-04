# _*_ coding:utf-8 _*_
__author__ = 'rapzhang'
__data__ = '2019/4/4 23:37'

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator



# 继承这个类会自动判断用户是否为登陆状态，如果不是返回/login/页面进行用户登陆
# 实际上就是给dispatch加装饰器增加一个用户判断登陆状态的功能而已

class LoginRequiredMixin(object):

    @method_decorator(login_required(login_url='/login/'))
    def dispatch(self,request,*args,**kwargs):
        return super(LoginRequiredMixin, self).dispatch(request,*args,**kwargs)

