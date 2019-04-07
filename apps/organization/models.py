from datetime import datetime

from django.db import models

# Create your models here.


class CityDict(models.Model):
    name = models.CharField(max_length=20,verbose_name=u'城市名')
    desc = models.CharField(max_length=200,verbose_name=u'描述')
    add_time = models.DateTimeField(default=datetime.now)

    class Meta:
        verbose_name = u'城市'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

# 课程机构基本信息 实体类
class CourseOrg(models.Model):
    name = models.CharField(max_length=50,verbose_name=u'机构名称')
    desc = models.TextField(verbose_name=u'机构描述')
    category = models.CharField(default='pxjg',max_length=20,choices=(('pxjg','培训机构'),('gx','高校'),('gr','个人')),verbose_name='机构类别')
    click_num = models.IntegerField(default=0,verbose_name=u'点击数')
    fav_nums = models.IntegerField(default=0,verbose_name=u'收藏数')
    image = models.ImageField(upload_to="org/%Y/%m",verbose_name=u'封面图',max_length=100)
    address = models.CharField(max_length=150,verbose_name=u'机构地址')
    # 涉及到城市搜索机构,会涉及到一对多的关系查询,引入外键
    city = models.ForeignKey(CityDict,verbose_name='所在城市')
    students = models.IntegerField(default=0,verbose_name=u'学习人数')
    course_nums = models.IntegerField(default=0,verbose_name=u'课程数')
    add_time = models.DateTimeField(default=datetime.now)

    class Meta:
        verbose_name = u'课程机构'
        verbose_name_plural = verbose_name

    def get_course_nums(self):
        return self.course_set.all().count()

    def get_teachers_nums(self):
        return self.teacher_set.all().count()

    def get_course_classic(self):
        return self.course_set.all()[:2]

    def __str__(self):
        return self.name

# 教师基本信息实体类
class Teacher(models.Model):
    org = models.ForeignKey(CourseOrg,verbose_name=u'所属机构')
    name = models.CharField(max_length=50,verbose_name=u'教师名称')
    work_years = models.IntegerField(default=0,verbose_name=u'工作年限')
    work_company = models.CharField(max_length=50,verbose_name=u'就职公司')
    work_position = models.CharField(max_length=50,verbose_name=u'公司职位')
    points = models.CharField(max_length=150,verbose_name=u'教学特点')
    click_num = models.IntegerField(default=0, verbose_name=u'点击数')
    fav_nums = models.IntegerField(default=0, verbose_name=u'收藏数')
    teacher_age = models.IntegerField('年龄',default=25)
    image = models.ImageField(
        default='teacher/default/timg.jpg',
        upload_to='teacher/%Y/%m',
        verbose_name='头像',
        max_length=100,
        null=True,
        blank=True
    )
    add_time = models.DateTimeField(default=datetime.now)
    # 缺少一个课程的外键

    class Meta:
        verbose_name = u'教师'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    def get_course_nums(self):
        return self.course_set.all().count()


