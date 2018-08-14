# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2018-08-09 02:17
from __future__ import unicode_literals

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='LogUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid', models.UUIDField(db_index=True, default=uuid.uuid4, unique=True)),
                ('account', models.CharField(max_length=32, unique=True, verbose_name='账号')),
                ('name', models.CharField(max_length=32, verbose_name='姓名')),
                ('password', models.CharField(max_length=80, verbose_name='密码')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('is_active', models.BooleanField(default=True, verbose_name='是否可用')),
            ],
            options={
                'verbose_name': 'Log用户',
                'verbose_name_plural': 'Log用户',
            },
        ),
    ]
