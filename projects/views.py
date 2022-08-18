import json

from django.http import HttpResponse, JsonResponse
from django.views import View
from django.shortcuts import render
from django.db import connection
from projects.models import Projects
from interfaces.models import Interfaces


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
        """
        一、创建（C）
        方式一：
        a.直接使用模型类(字段名1=值1， 字段名2=值2...)，创建模型类实例
        b.必须模型实例调用save()方法，才会执行sql语句
        obj = Projects(name='在线地产项目', leader='多喝热水')
        obj.save()
        方式二：
        a.使用模型类.objects返回manager对象
        b.使用manager对象.create(字段名1=值1，字段名2=值2，...)，来创建模型类实例
        c.无需使用模型实例调用save()方法，会自动执行sql语句
        obj = Projects.objects.create(name="xxx地产项目", leader="少喝凉水")
        """

        """
        二、读取(R)
        1、读取多种数据
        读取数据库中所有数据
        a.使用模型类.objects.all()，会将当前模型类对应的数据表中的所有数据读取出来
        b.模型类.objects.all()，返回QuerySet对象（查询集对象）
        c.QuerySet对象，类似于列表，具有惰性查询的特性（在'用'数据时，才会执行sql语句）
        qs = Projects.objects.all()
        2、读取单条数据
        a.可以使用模型类.objects.get(条件1=值1)
        b.如果使用指定条件查询的记录数量为0，会抛出异常
        c.如果使用指定条件查询的记录数量超过1，也会抛出异常
        d.最好使用唯一约束的条件去查询
        e.如果使用指定条件查询的记录数量为1，会返回这条记录对应的模型实例对象，可以使用模型对象.字段名去获取相应的字段值
        obj = Projects.objects.get(id=1)
        方式二：
        a.可以使用模型类.objects.filter(条件1=值1)，返回QuerySet对象
        b.如果使用指定条件查询的记录数量为0，会返回空的QuerySet对象
        c.如果使用指定条件查询的记录数量超过1，将符合条件的模型对象包裹到QuerySet对象中返回
        d.QuerySet对象类似于列表，有如下特性：
            1.支持通过数组（正整数）索引取值
            2.支持切片操作（正整数）
            3.获取第一个模型对象：QuerySet对象.first()
            4.获取最后一个模型对象：QuerySet对象.last()
            5.获取长度：len(querySet对象)、querySet对象.count()
            6.判断查询集是否为空：QuerySet对象.exists()
            7.支持迭代操作（for循环，每次循环返回模型对象）
        e.ORM框架中，会给每一个模型类中的主键设置一个别名（pk）
        filter方法支持多种查询类型
            1.字段名__查询类型=具体值
            2.字段名__exact=具体值，缩写形式为：字段名=具体值
            3.字段名__gt：大于、字段名__gte：大于等于
            4.字段名__lt：小于、字段名__lte：小于等于
            5.contains：包含
            6.startswith：以xxx开头
            7.endswith：以xxx结尾
            8.isnull：是否为null
            9.一般在查询类型前面加i，代表忽略大小写
        exclude为反向查询，filter方法支持的所有查询类型都支持
        """
        qs = Projects.objects.filter(id__lte=2)
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
