from django.contrib import admin
from User.models import *
# Register your models here.


class NodeDataAdmin(admin.ModelAdmin):
    list_per_page = 30
    list_display = ['id', 'd1', 'd2', 'd3', 'd4', 'd5', 'd6', 'd7', 'com']


class UserInfoAdmin(admin.ModelAdmin):
    list_per_page = 30
    list_display = ['id', 'username', 'password', 'create_time']


class IslandAdmin(admin.ModelAdmin):
    list_per_page = 30
    list_display = ['id', 'user_id_id']


class NodeAdmin(admin.ModelAdmin):
    list_per_page = 30
    list_display = ['id', 'island_id_id']


admin.site.register(UserInfo, UserInfoAdmin)
admin.site.register(Island, IslandAdmin)
admin.site.register(Node, NodeAdmin)
admin.site.register(NodeData, NodeDataAdmin)
