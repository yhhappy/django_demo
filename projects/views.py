import json

from django.db.models import Q, Count, Avg, Max, manager, QuerySet
from django.http import HttpResponse, JsonResponse
from django.views import View
from django.shortcuts import render
from django.db import connection
from projects.models import Projects
from interfaces.models import Interfaces
from projects.serializers import ProjectSerializer


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
    2.获取所有项目数据
    GET /projects/
    数据库操作（读取所有项目数据） -> 序列化输出操作（将模型对象转化为python中的基本类型）
    3.创建一条项目数据
    POST /projects/ 将项目数据以json格式来传递
    数据校验（规范传入的参数） -> 反序列化输入操作（将json格式的数据转化为复杂的类型） -> 数据库操作（创建项目数据）
    -> 序列化输出操作（将模型对象转化为python中的基本类型）
    """

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
        # 获取所有项目数据
        queryset = Projects.objects.all()
        serializer = ProjectSerializer(instance=queryset, many=True)
        return JsonResponse(serializer.data, safe=False)

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
        """
        1.获取json参数并转化为Python中的数据类型（字典）
        2.需要进行大量的数据校验
            a.需要校验必传参数是否有传递
            b.传递的有唯一约束的参数是否已存在
            c.必穿参数长度是否超过限制
            d.校验传参类型
        3.创建数据
        4.将创建成功的数据返回给前端
        """
        try:
            python_data = json.loads(request.body)
        except Exception as e:
            return JsonResponse({"msg": "参数有误"}, status=400)

        # project_data = Projects.objects.create(name=python_data.get("name"),
        #                                        leader=python_data.get("leader"),
        #                                        is_execute=python_data.get("is_execute"),
        #                                        desc=python_data.get("desc"))
        """
        反序列化操作
        1、定义序列化器类，使用data关键字参数传递字典参数
        2、可以使用序列化器对象调用.is_valid()方法，才会开始对前端输入的参数进行校验
        3、如果校验通过.is_valid()方法返回True，否则返回False
        4、如果调用.is_valid()方法，添加raise_exception=True，校验不通过会抛出异常，否则不会抛出异常
        5、只有在调用.is_valid()方法之后，才可以使用序列化器对象调用.errors属性，来获取错误提示信息（字典类型）
        6、只有在调用.is_valid()方法之后，才可以使用序列化器对象调用.validated_data属性，来获取校验通过之后的数据
        """
        serializer_in = ProjectSerializer(data=python_data)
        if not serializer_in.is_valid():
            return JsonResponse(serializer_in.errors, status=400)

        Projects.objects.create(**serializer_in.validated_data)
        return JsonResponse(serializer_in.data)


class ProjectsDetailView(View):
    """
        1.获取一条项目数据
        GET /projects/<int:pk>/
        4.更新一条项目数据
        PUT /projects/<int:pk>/
        5.删除一条项目数据
        DELETE /projects/<int:pk>/
        """
    def get(self, request, pk):
        # 1.需要校验pk在数据库中是否存在
        # 2.从数据库中读取项目数据
        try:
            python_data = Projects.objects.get(id=pk)
        except Exception as e:
            return JsonResponse({"msg": "参数有误"}, status=400)
        # python_dict = {
        #     'id': python_data.id,
        #     'name': python_data.name,
        #     'msg': '获取项目数据成功'
        # }
        serializer = ProjectSerializer(instance=python_data)
        return JsonResponse(serializer.data)

    def put(self, request, pk):
        # 1.需要校验pk在数据库中是否存在
        # 2.从数据库中读取项目数据
        try:
            project_obj = Projects.objects.get(id=pk)
        except Exception as e:
            return JsonResponse({"msg": "参数有误"}, status=400)
        # 3.获取json数据并转化为python中的数据类型（字典）
        try:
            python_data = json.loads(request.body)
        except Exception as e:
            return JsonResponse({"msg": "参数有误"}, status=400)
        serializer_in = ProjectSerializer(data=python_data)
        if not serializer_in.is_valid():
            return JsonResponse(serializer_in.errors, status=400)
        # 4.更新数据
        project_obj.name = serializer_in.validated_data.get("name")
        project_obj.leader = serializer_in.validated_data.get("leader")
        project_obj.is_execute = serializer_in.validated_data.get("is_execute")
        project_obj.desc = serializer_in.validated_data.get("desc")
        project_obj.save()
        # 5.将读取的项目数据转为字典
        python_dict = {
            'id': project_obj.id,
            'name': project_obj.name,
            'msg': '获取项目数据成功'
        }
        return JsonResponse(python_dict)

    def delete(self, request, pk):
        try:
            project_obj = Projects.objects.get(id=pk)
        except Exception as e:
            return JsonResponse({"msg": "参数有误"}, status=400)
        project_obj = Projects.objects.get(id=pk)
        project_obj.delete()
        return JsonResponse({"msg": "删除成功"}, status=204)




