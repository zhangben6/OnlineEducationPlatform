from datetime import datetime

from django.db import models

# Create your models here.
from users.models import UserProfile
from courses.models import Course


# 授课机构中'我要学习'弹窗实体类
class UserAsk(models.Model):
    name = models.CharField(max_length=20,verbose_name=u'姓名')
    mobile = models.CharField(max_length=11,verbose_name=u'手机号')
    course_name = models.CharField(max_length=50,verbose_name=u'课程名')
    add_time = models.DateTimeField(default=datetime.now,verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'用户咨询'
        verbose_name_plural = verbose_name


# 课程评论实体类
class CourseComments(models.Model):
    user = models.ForeignKey(UserProfile,verbose_name=u'用户')
    course = models.ForeignKey(Course,verbose_name=u'课程')
    comments = models.CharField(max_length=20,verbose_name=u'评论内容')
    add_time = models.DateTimeField(default=datetime.now,verbose_name=u'添加时间')


    class Meta:
        verbose_name = u'课程评论'
        verbose_name_plural = verbose_name


# 用户收藏的课程及讲师及课程机构
class UserFavorite(models.Model):
    user = models.ForeignKey(UserProfile,verbose_name=u'用户')
    fav_id = models.IntegerField(default=0,verbose_name=u'数据id')
    fav_type = models.IntegerField(choices=((1,'课程'),(2,'课程机构'),(3,'讲师')),default=1,verbose_name=u'收藏类型')
    add_time = models.DateTimeField(default=datetime.now,verbose_name=u'添加时间')


    class Meta:
        verbose_name = u'用户收藏'
        verbose_name_plural = verbose_name



# 用户消息
class UserMessage(models.Model):
    # 发送消息操作,代表的接收用户
    user = models.IntegerField(default=0,verbose_name=u'接收用户')
    message = models.CharField(max_length=500,verbose_name=u'消息内容')
    has_read = models.BooleanField(default=False,verbose_name=u'是否已读')
    add_time = models.DateTimeField(default=datetime.now,verbose_name=u'添加时间')


    class Meta:
        verbose_name = u'用户消息'
        verbose_name_plural = verbose_name


# 用户收藏学习的课程信息
class UserCourse(models.Model):
    user = models.ForeignKey(UserProfile, verbose_name=u'用户')
    course = models.ForeignKey(Course, verbose_name=u'课程')
    add_time = models.DateTimeField(default=datetime.now,verbose_name=u'添加时间')


    class Meta:
        verbose_name = u'用户课程'
        verbose_name_plural = verbose_name








