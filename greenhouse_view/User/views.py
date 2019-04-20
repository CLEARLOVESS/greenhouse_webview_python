from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from User import models
from django.views.decorators.csrf import csrf_exempt
import re


# Create your views here.
global temp_username
temp_username = ''
global temp_password
temp_password = ''


# /login 默认登录login
def login(request):
    return render(request, 'login.html')


# /login_check 登录检查
@csrf_exempt
def login_check(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    if not all([username, password]):
        return JsonResponse({'res': 0})
    try:
        if models.UserInfo.objects.get(username=username, password=password):
            print('>>>   用户登录成功--用户名--密码--', username, password)
            global temp_username
            temp_username = username
            global temp_password
            temp_password = password
            return JsonResponse({'res': 1})
        else:
            print('>>>   用户登录失败!')
            return JsonResponse({'res': 0})
    except Exception as err:
        print('>>>   登录检查失败,错误--', err)
        return JsonResponse({'res': 0})


# /register 注册页面
def register(request):
    return render(request, 'register.html')


# /register_check 注册检查
@csrf_exempt
def register_check(request):
    try:
        username = request.POST.get('username')
        password = request.POST.get('password')
        if not all([username, password]):
            return JsonResponse({'res': 0})
        try:
            if models.UserInfo.objects.get(username=username):
                print('>>>   用户名已经存在,请重新注册!')
                return JsonResponse({'res': 2})
        except Exception as err:
            print('>>>   错误提示---', err)
        u = models.UserInfo()
        u.username = username
        u.password = password
        u.save()
        print('>>>   注册成功--用户名--密码--', username, password)
        return JsonResponse({'res': 1})
    except Exception as res:
        print(">>>   注册失败!---", res)
        return JsonResponse({'res': 0})


# 数据页面
def index(request):
    return render(request, 'index.html')


# 传json
@csrf_exempt
def index_check(request):
    # 依据id排序
    print('>>>   进入index_check')
    try:
        com = request.POST.get('com')
        if re.match(r'^com\d+|COM\d+$', com):
            nd = models.NodeData.objects.filter(com=com).order_by('-id')
            d1 = nd[0].d1
            d2 = nd[0].d2
            d3 = nd[0].d3
            d4 = nd[0].d4
            d5 = nd[0].d5
            d6 = nd[0].d6
            d7 = nd[0].d7
            print('>>>   取到数据!', d1, d2, d3, d4, d5, d6, d7, com)
            return JsonResponse({'d1': d1, 'd2': d2, 'd3': d3, 'd4': d4, 'd5': d5, 'd6': d6, 'd7': d7, 'res': 1})
        else:
            print('>>>   请输入正确的COM端口!')
            return JsonResponse({'res': 0})
    except Exception as err:
        print('>>>   读取数据失败,请检查COM端口是否有效!---', err)
        return JsonResponse({'res': 0})


# /user_info
@csrf_exempt
def user_info(request):
    global temp_password
    global temp_username
    username = temp_username
    password = temp_password
    return render(request, 'user_info.html', {'username': username, 'password': password})


# /change_password
def change_password(request):
    return render(request, 'change_password.html')


# /changepassword_check
@csrf_exempt
def changepassword_check(request):
    try:
        username = request.POST.get('username')
        new_password = request.POST.get('new_password')
        renew_password = request.POST.get('renew_password')
        u = models.UserInfo.objects.get(username=username)
        if new_password == renew_password:
            u.password = new_password
            u.save()
            return JsonResponse({'res': 1})
        else:
            return JsonResponse({"res": 0})
    except Exception as err:
        print('>>>   修改密码错误!---', err)
        return JsonResponse({"res": 0})


def password_success(request):
    return render(request, 'password_success.html')

