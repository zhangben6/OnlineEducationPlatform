# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-04-04 16:56
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0009_auto_20190331_2142'),
        ('courses', '0010_auto_20190404_1644'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='teacher',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='organization.Teacher', verbose_name='授课老师'),
        ),
    ]
