# _*_ coding:utf-8 _*_
__author__ = 'rapzhang'
__data__ = '2019/3/31 12:06'
import re
from django import forms

from operation.models import UserAsk


# 如果不使用ModelForm定义实体类的表单，代码重写几率大
# class UserAskForm(forms.Form):
#     name = forms.CharField(required=True,min_length=2,max_length=15)
#     phone = forms.CharField(required=True,min_length=11,max_length=11)
#     course_name = forms.CharField(required=True,mix_length=5,max_length=50)



# 特殊情况: 如果实体类model的字段和Form实体类的字段相似，那么直接可以把Model转换成Form实体类
class UserAskForm(forms.ModelForm):
    '''
    1.这个类不光可以继承Model的字段，还是在此基础上新增加一些字段
      如: my_filed = forms.CharField(xxx)
    2. 这个ModelForm实体类对象可以直接调用.save()方法将数据保存到数据库，调用meta信息中实体类的方法
    '''
    class Meta:  # 此Meta声明的信息是需要将哪个Model转换称Form实体类
        model = UserAsk
        # 自定义选择需求字段
        fields = ['name','mobile','course_name']

    def clean_mobile(self):
        '''
        通过自定义正则表达式验证手机号的格式
        '''
        mobile = self.cleaned_data['mobile']
        mobile = str(mobile)
        # 进行正则表达式的匹配
        REGEX_MOBILE = "^1[358]\d{9}$|^147\d{8}$|176\d{8}$"
        p = re.compile(REGEX_MOBILE)
        if p.match(mobile):
            return mobile
        else:
            raise forms.ValidationError(u"手机号码非法", code="mobile_invalid")