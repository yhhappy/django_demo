import json

from django.http import HttpResponse, JsonResponse
from django.views import View
from django.shortcuts import render
from django.db import connection
from projects.models import Projects


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
    c.视图函数必须返回一个HttpResponse对象或者其子类对象
    :param request:
    :return:
    '''
    # print(request)
    # print(type(request))
    # print(type(request).__mro__)
    if request.method == 'GET':
        return HttpResponse('<h1>获取项目信息</h1>')
    if request.method == 'POST':
        return HttpResponse('<h1>创建项目信息</h1>')
    if request.method == 'PUT':
        return HttpResponse('<h1>更新项目信息</h1>')
    if request.method == 'DELETE':
        return HttpResponse('<h1>删除项目信息</h1>')
    else:
        return HttpResponse('<h1>其他操作</h1>')


class ProjectsView(View):
    """
    一、定义类视图
    1、继承View或者View子类
    2、不同的请求方法有相应的方法进行对应
        GET -> get
        POST -> post
        PUT -> put
        DELETE -> delete
        PATCH -> patch
    3.每一个处理请求的方法，必须得返回HttpResponse对象或者HttpResponse子类对象
    4.每一个处理请求的方法，第二个参数必须为HttpRequest对象
    5.HttpResponse
        a.第一个参数为字符串类型（需要返回到前端的字符串数据）
        b.content_type可以指定响应头中的Content_Type参数
        c.status可以指定响应状态码
    6.JsonResponse
        a.为HttpResponse子类
        b.用于返回json数据
        c.第一个参数可以直接传递字典或者嵌套字典的列表
        d.默认添加content_type为application/json
        e.默认第一个参数只能为字典，如果为嵌套字典的列表，需要设置safe=False
    7.两种开发模式
        1）前后端不分离的开发模式
            后端结果返回的是一个完整的html页面（页面中有填充数据）
        2）前后端分离的开发模式
            后端结果返回的是数据(json、xml)
    """
    def get(self, request):
        # 一、创建（C）
        # 方式一：
        # a.直接使用模型类
        # obj = Projects(name='在线地产项目', leader='多喝热水')
        # obj.save()
        # 方式二：
        obj = Projects.objects.create(name="xxx读书项目", leader="少喝凉水")
        pass

        # project_data = {
        #     'id': 1,
        #     'name': 'xxx项目',
        #     'leader': 'yang'
        # }
        # project_data_list = [
        #     {
        #         'id': 1,
        #         'name': 'xxx项目',
        #         'leader': 'yang'
        #     },
        #     {
        #         'id': 2,
        #         'name': 'xxx项目',
        #         'leader': 'hang'
        #     }
        # ]
        # json_str = json.dumps(project_data, ensure_ascii=False)
        # return HttpResponse(json_str, content_type='application/json', status=201)
        # return JsonResponse(project_data, json_dumps_params={'ensure_ascii': False})
        # print(request)
        # return JsonResponse(project_data_list, json_dumps_params={'ensure_ascii': False}, status=201, safe=False)

    def post(self, request):
        """
        前端参数解析
        前端传递参数的方式
        1、路径参数
            a.在url路径中传递的参数
            b.在请求实例方法中使用关键字参数来接收
        2、查询字符串参数
            a. url ? 后面的key value 键值对参数，如 http://www.xxx.com/?key1=value1&key2=value2
            b. request.GET获取
            c. request.GET返回QueryDict，类似于python中dict类型
            d. 可以使用['key1']、get('key1')，会返回具体的值，如果有多个相同key的键值对，获取的是最后一个
            e. getlist('key1')，获取相同key的多个值，返回list类型
        3、请求体参数
            1) json
                a. json格式的参数会存放在body中，一般为字节类型
                b. json.loads(request.body)，返回python中的数据类型（字典、嵌套字典的列表）
            2) x-www-form-urlencoded
                a. 一般在前端页面中使用表单录入的参数
                b. request.POST返回QueryDict，类似于python中dict类型
            3) file （multipart/data）
                a. 传递的文本参数可以使用request.POST去获取
                b. 传递的非文本参数（二进制文件）可以使用request.FILES去提取
                c. 如果传递纯粹的文件，request.body去提取

        请求头参数
            a. 第一种方式： request.headers['key1']或者get('key1')
            b. 第二种方式： request.META['HTTP_AUTHORIZATION']
                1) 请求头参数可以转化为：HTTP_参数名大写
                2） 如果参数名含有-，会自动转换为_

        """
        print(request)
        return HttpResponse('<h1>创建项目信息</h1>')

    def put(self, request):
        return HttpResponse('<h1>更新项目信息</h1>')

    def delete(self, request):
        return HttpResponse('<h1>删除项目信息</h1>')
