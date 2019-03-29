# coding:utf-8
from datetime import datetime

from django.db import models
# 继承django自带数据库中的auth_user表
from django.contrib.auth.models import AbstractUser

# Create your models here.


# 用户信息表,自定义实体类继承auth_user表
class UserProfile(AbstractUser):
    nick_name = models.CharField(max_length=50,verbose_name=u'昵称',default=u'')
    birthday = models.DateField(verbose_name=u'生日',null=True,blank=True) # 后面两个值允许为空
    gender = models.CharField(max_length=6,choices=(("male",'男'),('female','女')),default='female')
    address = models.CharField(max_length=100,default=u'')
    mobile = models.CharField(max_length=11,null=True,blank=True)
    image = models.ImageField(upload_to="user_image/%Y/%m",default=u'user_image/default.png',max_length=100)

    class Meta:
        verbose_name = '用户信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username

# 邮箱验证码实体类
class EmailVerifyRecord(models.Model):
    code = models.CharField(max_length=20,verbose_name=u'验证码字串') # 如果不设置null=Ture的话,默认不允许为空
    email = models.CharField(max_length=50,verbose_name=u'邮箱')
    send_type = models.CharField(verbose_name=u'验证码类型',choices=(('register',u'注册'),('forget',u'找回密码')),max_length=10)
    send_time = models.DateTimeField(verbose_name=u'发送时间',default=datetime.now)

    class Meta:
        verbose_name = '邮箱验证码'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '{0}({1})'.format(self.code,self.email)

# 首页轮播图实体类
class Banner(models.Model):
    title = models.CharField(max_length=100,verbose_name=u'标题')
    image = models.ImageField(upload_to="banner/%Y/%m",verbose_name=u'轮播图',max_length=100) # 存放路径
    url = models.URLField(max_length=200,verbose_name=u'访问地址')
    index = models.IntegerField(default=100,verbose_name=u'顺序')
    add_time = models.DateTimeField(default=datetime.now,verbose_name=u'添加时间')

    class Meta:
        verbose_name = '轮播图'
        verbose_name_plural = verbose_name



