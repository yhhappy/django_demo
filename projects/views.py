from django.http import HttpResponse
from django.shortcuts import render


# 在views.py中定义的函数，称为视图函数
def create_project(request):
    return HttpResponse('<h1>创建项目信息</h1>')


def put_project(request, pk):
    return HttpResponse('<h1>更新项目信息</h1>')


def delete_project(request):
    return HttpResponse('<h1>删除项目信息</h1>')


def get_projects(request, pk):
    return HttpResponse(f'<h1>获取项目{pk}信息</h1>')


def projects(request):
    '''
    视图函数
    a.视图函数的第一参数是HttpRequest对象
    b.HttpRequest对象包含了请求的所有数据（请求头、请求体）
    :param request:
    :return:
    '''
    print(request)
    print(type(request))
    print(type(request).__mro__)
    return HttpResponse('<h1>获取项目信息test</h1>')
