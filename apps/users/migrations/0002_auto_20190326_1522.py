# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-03-26 15:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='banner',
            name='image',
            field=models.ImageField(upload_to='media/banner/%Y/%m', verbose_name='轮播图'),
        ),
    ]
