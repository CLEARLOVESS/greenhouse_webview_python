from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from User import models
from django.views.decorators.csrf import csrf_exempt

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
            print('---username  have')
            global temp_username
            temp_username = username
            global temp_password
            temp_password = password
            return JsonResponse({'res': 1})
        else:
            print('---username is null')
            return JsonResponse({'res': 0})
    except:
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
        print(username, password)
        u = models.UserInfo()
        u.username = username
        u.password = password
        u.save()
        print("---注册成功")
        return JsonResponse({'res':1})
    except Exception as res:
        print("---注册失败", res)
        return JsonResponse({'res':0})


# 数据页面
def index(request):
    return render(request, 'index.html')


# 传json
@csrf_exempt
def index_check(request):
    # 依据id排序
    print('---进入index_check')
    try:
        com = request.POST.get('com')
        if com:
            nd = models.NodeData.objects.order_by('-id')
            d1 = nd[0].d1
            d2 = nd[0].d2
            d3 = nd[0].d3
            d4 = nd[0].d4
            d5 = nd[0].d5
            d6 = nd[0].d6
            d7 = nd[0].d7
            print('---有数据', d1, d2, d3, d4, d5, d6, d7, com)
            return JsonResponse({'d1': d1, 'd2': d2, 'd3': d3, 'd4': d4, 'd5': d5, 'd6': d6, 'd7': d7, 'res': 1})
        else:
            return JsonResponse({'res': 0})
    except Exception as r:
        print('错误提示', r)
        return JsonResponse({'res': 0})


# /user_info
@csrf_exempt
def user_info(request):
    global temp_password
    global temp_username
    username = temp_username
    password = temp_password
    # temp_password = ''
    # temp_username = ''
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
    except Exception as re:
        print('出错了', re)
        return JsonResponse({"res": 0})


def password_success(request):
    return render(request, 'password_success.html')

