# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-04-01 23:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20190326_1538'),
    ]

    operations = [
        migrations.AlterField(
            model_name='banner',
            name='image',
            field=models.ImageField(upload_to='banner/%Y/%m', verbose_name='轮播图'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='image',
            field=models.ImageField(default='user_image/default.png', upload_to='user_image/%Y/%m'),
        ),
    ]