# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-03-31 14:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('operation', '0002_auto_20190331_1418'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userask',
            name='mobile',
            field=models.CharField(max_length=11, verbose_name='手机号'),
        ),
    ]