from django.db import models

# Create your models here.


# 用户表 注册用户用
class UserInfo(models.Model):

    # id自动生成
    # 姓名
    username = models.CharField(max_length=20, verbose_name='姓名')

    # 密码
    password = models.CharField(max_length=20, verbose_name='密码')

    # 注册时间
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='注册时间')

    # 定义表名
    class Meta:
        db_table = 'userinfo'


# 土地表 用户的土地所有权
class Island(models.Model):
    # 用户外键
    user_id = models.ForeignKey('UserInfo', verbose_name='用户外键')

    # 定义表名
    class Meta:
        db_table = 'island'


# 节点表 传感器
class Node(models.Model):
    # 土地外键
    island_id = models.ForeignKey('Island', verbose_name='土地外键')

    # 定义表名
    class Meta:
        db_table = 'node'


# 节点数据表
class NodeData(models.Model):
    # 湿度
    d1 = models.CharField(max_length=5, verbose_name='湿度(%rh)')
    # 温度
    d2 = models.CharField(max_length=5, verbose_name='温度(℃)')
    # 土壤湿度
    d3 = models.CharField(max_length=5, verbose_name='土壤湿度(%rh)')
    # PM2.5
    d4 = models.CharField(max_length=5, verbose_name='PM2.5(微克/每立方米)')
    # CO2
    d5 = models.CharField(max_length=5, verbose_name='CO2(ppm)')
    # 气体浓度
    d6 = models.CharField(max_length=5, verbose_name='气体浓度(ppm)')
    # 光照强度
    d7 = models.CharField(max_length=5, verbose_name='光照强度(lx)')
    # 属于哪个com端口
    com = models.CharField(max_length=10, verbose_name='COM端口')
    # 创建时间
    # create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    # 节点id外键
    # node_id = models.ForeignKey('Node')

    # 定义表名
    class Meta:
        db_table = 'nodedata'





