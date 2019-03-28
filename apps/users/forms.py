# _*_ coding:utf-8 _*_
__author__ = 'rapzhang'
__data__ = '2019/3/28 12:24'
from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(required=True,error_messages={'required': '手机号必填项'})
    password = forms.CharField(required=True,
                                min_length=6,
                               error_messages={'min_length': '输入的字符要大于6','required':'不能为空，熊dei'}
                               )

