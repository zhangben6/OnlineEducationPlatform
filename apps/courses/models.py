from datetime import datetime

# Create your models here.
from django.db import models
from organization.models import CourseOrg,Teacher


# 课程详情页实体类
class Course(models.Model):
    course_org = models.ForeignKey(CourseOrg,verbose_name='课程机构',null=True,blank=True)
    name = models.CharField(max_length=50,verbose_name=u'课程名称')
    desc = models.CharField(max_length=300,verbose_name=u'课程描述')
    detail = models.TextField(verbose_name=u'课程详情') # 课程详情介绍
    degree = models.CharField(verbose_name='课程难度',choices=(('cj','初级'),('zj','中级'),('gj','高级')),max_length=2) # 课程难度
    learn_times = models.IntegerField(default=0,verbose_name=u'学习时长(分钟数)')
    students = models.IntegerField(default=0,verbose_name=u'学习人数')
    fav_nums = models.IntegerField(default=0,verbose_name=u'收藏人数')
    image = models.ImageField(upload_to="courses/%Y/%m",verbose_name=u'封面图',max_length=100,null=True,blank=True)
    tag = models.CharField(default='',verbose_name=u'课程标签',max_length=10)
    category = models.CharField(max_length=20,default=u'后端开发',verbose_name=u'课程类别')
    num_click = models.IntegerField(default=0,verbose_name='点击数')
    teacher = models.ForeignKey(Teacher,verbose_name=u'授课老师',null=True,blank=True)
    need_know = models.CharField(max_length=100,default='',null=True,blank=True,verbose_name=u'课程须知')
    teacher_all = models.CharField(max_length=100,default='',null=True,blank=True,verbose_name=u'老师告诉你')
    is_banner = models.BooleanField(default=False,verbose_name=u'是否轮播')
    add_time = models.DateTimeField(default=datetime.now,verbose_name='添加时间')

    class Meta:
        verbose_name = u'课程'
        verbose_name_plural = verbose_name

    def get_zj_nums(self):
        # 获取课程章节数
        return self.lesson_set.all().count()
    get_zj_nums.short_description = '章节数'

    # 显示在xadmin后台页面进行跳转
    def go_to(self):
        from django.utils.safestring import mark_safe
        return mark_safe("<a href='https://www.baidu.com'>跳转百度 </a>'")
    go_to.short_description = '跳转'

    def get_learn_user(self):
        return self.usercourse_set.all()[:5]

    def get_course_lesson(self):
        # 获取所有章节信息
        return self.lesson_set.all()

    def __str__(self):
        return self.name

class BannerCourse(Course):
     class Meta:
         verbose_name = '轮播课程'
         verbose_name_plural = verbose_name
         proxy = True



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


    #  通过外键获取章节的所有视频
    def get_lesson_video(self):
        return self.video_set.all()


# 视频播放地址实体类
class Video(models.Model):
    lesson = models.ForeignKey(Lesson,verbose_name=u'章节')
    url = models.CharField(max_length=200,default='',verbose_name=u'访问地址')
    name = models.CharField(max_length=100,verbose_name=u'视频名称')
    learn_times = models.IntegerField(default=0, verbose_name=u'学习时长(分钟数)')
    add_time = models.DateTimeField(default=datetime.now,verbose_name='添加时间')

    class Meta:
        verbose_name = u'视频'
        verbose_name_plural = verbose_name


# 课程资源
class CourseResource(models.Model):
    course = models.ForeignKey(Course,verbose_name=u'课程')
    name = models.CharField(max_length=100, verbose_name=u'资源名称')
    download = models.FileField(upload_to="course/resource/%Y/%m",verbose_name=u"资源文件",max_length=100)
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = u'课程资源'
        verbose_name_plural = verbose_name



