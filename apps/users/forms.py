# _*_ coding:utf-8 _*_
__author__ = 'rapzhang'
__data__ = '2019/3/28 12:24'
from django import forms
from captcha.fields import CaptchaField

from .models import UserProfile


class LoginForm(forms.Form):
    username = forms.CharField(required=True,error_messages={'required': '手机号必填项'})
    password = forms.CharField(required=True,
                                min_length=6,
                               error_messages={'min_length': '输入的字符要大于6','required':'不能为空，熊dei'}
                               )


class RegisterForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True)
    captcha = CaptchaField(error_messages={'invalid':u'验证码错误!'})


class ForgetForm(forms.Form):
    email = forms.EmailField(required=True)
    captcha = CaptchaField(error_messages={'invalid': u'验证码错误!'})


class ModifyPwdForm(forms.Form):
    password1 = forms.CharField(required=True,min_length=6)
    password2 = forms.CharField(required=True,min_length=6)


class UploadImageForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        # 自定义选择需求字段
        fields = ['image']


class UserInfoForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['nick_name','gender','birthday','address','mobile']

