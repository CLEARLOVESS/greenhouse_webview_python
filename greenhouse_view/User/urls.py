from django.conf.urls import url
from User import views

urlpatterns = [

    # 注册
    url(r'^register$', views.register),
    url(r'^register_failed$', views.register_failed),
    url(r'^register_check$', views.register_check),

    # 主页
    url(r'^index$', views.index),
    url(r'^index_check$', views.index_check),

    # 用户中心
    url(r'^user_info$', views.user_info),
    # 修改密码
    url(r'^change_password$', views.change_password),
    url(r'^changepassword_check$', views.changepassword_check),

    # 登录和登录校验
    url(r'^login$', views.login),
    url(r'^login_check$', views.login_check),
    url(r'', views.test),  # 默认login
],