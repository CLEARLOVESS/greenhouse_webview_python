"""greenhouse_view URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from User import views

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),

    # 注册
    url(r'^register$', views.register),
    url(r'^register_check$', views.register_check),

    # 主页
    url(r'^index$', views.index),
    url(r'^index_check$', views.index_check),

    # 用户中心
    url(r'^user_info$', views.user_info),
    # 修改密码
    url(r'^change_password$', views.change_password),
    url(r'^changepassword_check$', views.changepassword_check),
    url(r'^password_success$', views.password_success),

    # 登录和登录校验
    url(r'^login$', views.login),
    url(r'^login_check$', views.login_check),
    url(r'^$', views.login),  # 默认login
]
