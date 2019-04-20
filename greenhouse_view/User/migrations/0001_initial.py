# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Island',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
            ],
            options={
                'db_table': 'island',
            },
        ),
        migrations.CreateModel(
            name='Node',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('island_id', models.ForeignKey(verbose_name='土地外键', to='User.Island')),
            ],
            options={
                'db_table': 'node',
            },
        ),
        migrations.CreateModel(
            name='NodeData',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('d1', models.CharField(verbose_name='湿度(%rh)', max_length=5)),
                ('d2', models.CharField(verbose_name='温度(℃)', max_length=5)),
                ('d3', models.CharField(verbose_name='土壤湿度(%rh)', max_length=5)),
                ('d4', models.CharField(verbose_name='PM2.5(微克/每立方米)', max_length=5)),
                ('d5', models.CharField(verbose_name='CO2(ppm)', max_length=5)),
                ('d6', models.CharField(verbose_name='气体浓度(ppm)', max_length=5)),
                ('d7', models.CharField(verbose_name='光照强度(lx)', max_length=5)),
                ('com', models.CharField(verbose_name='COM端口', max_length=10)),
            ],
            options={
                'db_table': 'nodedata',
            },
        ),
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('username', models.CharField(verbose_name='姓名', max_length=20)),
                ('password', models.CharField(verbose_name='密码', max_length=20)),
                ('create_time', models.DateTimeField(verbose_name='注册时间', auto_now_add=True)),
            ],
            options={
                'db_table': 'userinfo',
            },
        ),
        migrations.AddField(
            model_name='island',
            name='user_id',
            field=models.ForeignKey(verbose_name='用户外键', to='User.UserInfo'),
        ),
    ]
