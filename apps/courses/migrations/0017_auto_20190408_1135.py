# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-04-08 11:35
from __future__ import unicode_literals

import DjangoUeditor.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0016_auto_20190408_1131'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='desc',
            field=models.CharField(max_length=300, verbose_name='课程描述'),
        ),
        migrations.AlterField(
            model_name='course',
            name='detail',
            field=DjangoUeditor.models.UEditorField(default='', verbose_name='课程详情'),
        ),
    ]
