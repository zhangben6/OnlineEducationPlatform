# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-04-03 13:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0005_course_shabi'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course',
            name='shabi',
        ),
        migrations.AddField(
            model_name='course',
            name='num_click',
            field=models.IntegerField(default=0, verbose_name='点击数'),
        ),
    ]
