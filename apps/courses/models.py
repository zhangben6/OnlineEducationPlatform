from datetime import datetime

# Create your models here.
from django.db import models


# 课程详情页实体类
class Course(models.Model):
    name = models.CharField(max_length=50,verbose_name=u'课程名称')
    desc = models.CharField(max_length=300,verbose_name=u'课程描述')
    detail = models.TextField(verbose_name=u'课程详情') # 课程详情介绍
    degree = models.CharField(verbose_name='课程难度',choices=(('cj','初级'),('zj','中级'),('gj','高级')),max_length=2) # 课程难度
    learn_times = models.IntegerField(default=0,verbose_name=u'学习时长(分钟数)')
    students = models.IntegerField(default=0,verbose_name=u'学习人数')
    fav_nums = models.IntegerField(default=0,verbose_name=u'收藏人数')
    image = models.ImageField(upload_to="media/courses/%Y/%m",verbose_name=u'封面图',max_length=100)
    click_nums = models.IntegerField(default=0,verbose_name=u'点击数')
    add_time = models.DateTimeField(default=datetime.now,verbose_name='添加时间')

    class Meta:
        verbose_name = u'课程'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


# 章节信息实体类
class Lesson(models.Model):
    # 一(course) 对 多(lesson) 关系,在多的实体类中添加外键
    course = models.ForeignKey(Course,verbose_name=u'课程')
    name = models.CharField(max_length=100,verbose_name=u'章节名')
    add_time = models.DateTimeField(default=datetime.now,verbose_name='添加时间')

    class Meta:
        verbose_name = u'章节'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


# 视频播放地址实体类
class Video(models.Model):
    lesson = models.ForeignKey(Lesson,verbose_name=u'章节')
    name = models.CharField(max_length=100,verbose_name=u'视频名称')
    add_time = models.DateTimeField(default=datetime.now,verbose_name='添加时间')

    class Meta:
        verbose_name = u'视频'
        verbose_name_plural = verbose_name


# 课程资源
class CourseResource(models.Model):
    course = models.ForeignKey(Course,verbose_name=u'课程')
    name = models.CharField(max_length=100, verbose_name=u'资源名称')
    download = models.FileField(upload_to="media/course/resource/%Y/%m",verbose_name=u"资源文件",max_length=100)
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = u'课程资源'
        verbose_name_plural = verbose_name



