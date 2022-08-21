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
    1.获取一条项目数据
    GET /projects/<int:pk>/
    2.获取所有项目数据
    GET /projects/
    数据库操作（读取所有项目数据） -> 序列化输出操作（将模型对象转化为python中的基本类型）
    3.创建一条项目数据
    POST /projects/ 将项目数据以json格式来传递
    数据校验（规范传入的参数） -> 反序列化输入操作（将json格式的数据转化为复杂的类型） -> 数据库操作（创建项目数据）
    -> 序列化输出操作（将模型对象转化为python中的基本类型）
    4.更新一条项目数据
    PUT /projects/<int:pk>/
    5.删除一条项目数据
    DELETE /projects/<int:pk>/
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
        # project_list = []
        # for item in queryset:
        #     item: Projects
        #     project_dict = {
        #         'id': item.id,
        #         'name': item.name,
        #         'leader': item.leader
        #     }
        #     project_list.append(project_dict)
        """
        序列化器的使用
        1.可以使用序列化器进行序列化输出操作
            a.创建序列化器对象
            b.可以将模型对象或者查询集对象、普通对象、嵌套普通对象的列表，以instance关键字来传递参数
            c.如果传递的是查询集对象，嵌套普通对象的列表（多条数据），需要设置many=True
            d.如果传递的是模型对象、普通对象，不需要设置many=True
            f.可以使用序列化器对象的.data属性，获取序列化器之后的数据（字典、嵌套字典的列表）
        """
        serializer = ProjectSerializer(instance=queryset, many=True)
        return JsonResponse(serializer.data, safe=False)

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
        # qs = Projects.objects.filter(id__lte=2)
        # pass
        """
        创建从表数据，外键对应的父表如何传递？
        方式一：
        1.先获取父表模型对象
        2.将获取的父表模型对象以外键字段名作为参数来传递
        project_obj = Projects.objects.get(name='在线图书项目')
        Interfaces.objects.create(name='在线图书项目-登录接口', tester='呼呼', projects=project_obj)
        方式二：
        1.先获取父表模型对象，进而获取父表数据的id值
        2.将父表数据的主键值以外键名_id作为参数来传递
        project_obj = Projects.objects.get(name='在线金融项目')
        Interfaces.objects.create(name='在线金融项目-注册接口', tester='呼呼', projects_id=project_obj.id)
        
        通过从表模型对象（已经获取到了），如何获取父表数据？
        可以通过外键字段先获取父表模型对象
        interface_obj = Interfaces.objects.get(id=1)
        name = interface_obj.projects.name
        
        通过父表模型对象（已经获取到了），如何获取从表数据？
        默认可以通过从表模型类名小写_set，返回manager对象，可以进一步使用filter进行过滤
        project_obj = Projects.objects.get(id=1)
        project_obj.interfaces_set.all()
        如果在从表模型类的外键字段指定了related_name参数，related=inter,那么会使用related_name指定参数作为名称
        project_obj = Projects.objects.get(id=1)
        project_obj.inter.all()
        
        如果想要通过父表参数来获取从表数据、想要通过从表参数获取父表数据 --- 关联查询
        可以使用关联查询语句：
        关联字段名称_关联模型类中的字段名称_查询类型
        Interfaces.objects.filter(projects__name__contains='图书')
        Projects.objects.filter(interfaces__name__contains="登录")
        
        逻辑关系
        与关系
        方式一：
        在同一个filter方法内部，添加多个关键字参数，那么每个条件是“与”关系
        Projects.objects.filter(name__contains='图书', leader='少喝凉水')
        方式二：
        可以多次调用filter方法，那么filter方法的条件为“与”关系 --- QuerySet链式调用特性
        Projects.objects.filter(name__contains='项目').filter(leader='多喝热水')
        
        或关系
        可以使用Q查询，实现逻辑关系，多个Q对象之间如果使用“|”，那么为“或”关系
        qs = Projects.objects.filter(Q(name__contains="图书") | Q(leader="多喝热水"))
        
        排序（QuerySet）
        可以使用QuerySet对象（manager对象）.order_by('字段名1', '字段名2', '-字段3')
        默认为ASC升序，可以在字段名称前添加“-”，那么为DESC降序
        Projects.objects.filter(Q(name__contains="图书") | Q(leader="多喝热水")).order_by("-id", "leader")
        
        三、更新（U）
        方式一：
        project_obj = Projects.objects.get(id=1)
        project_obj.name = "在线图书项目（一期）"
        project_obj.leader = "哈哈"
        1.必须调用save方法才会执行sql语句，并且默认进行完整更新
        project_obj.save()
        2.可以在save方法中设置update_fields参数（序列类型），指定需要更新的字段名称（字符串）
        project_obj.save(update_fields=["name", "leader"])
        方式二：
        可以在QuerySet对象.update(字段名称=“字段值”)，返回修改成功的值，无需调用save方法
        Projects.objects.filter(name__contains='金融').update(leader="金算盘")
        
        四、删除（D）
        方式一：一条数据
        project_obj = Projects.objects.get(id=1)
        project_obj.delete()
        方式二：多条数据
        Projects.objects.filter(name__contains="图书").delete()
        """
        """
        聚合运算
        a.可以使用QuerySet对象，aggregate(聚合函数('字段名'))方法，返回字典数据
        b.返回的字典数据中key为字段名__聚合函数名小写
        c.可以使用关键字参数形式，那么返回的字典数据中key为关键字参数名
        Projects.objects.filter(name__contains="项目").aggregate(Count('id'))
        """
        """
        分组查询
        a.可以使用QuerySet对象.values('父表主键id').annotate(聚合函数('从表模型类名小写'))
        b.会自动连接两张表，然后使用外键字段作为分组条件
        qs = Projects.objects.values('id').annotate(Count('interfaces'))
        
        查询集QuerySet有什么特性？
        1.支持链式调用，可以在查询集上多次调用filter、exclude方法
        2.惰性查询：仅仅在使用数据时才会执行sql语句，为了提升数据库读写性能
        会执行sql语句的场景：len() count() 通过索引取值 print for
        """

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
        """
        serializer_in = ProjectSerializer(data=python_data)
        serializer_in.is_valid()
        project_data = Projects.objects.create(**python_data)
        python_dict = {
            'id': project_data.id,
            'name': project_data.name,
            'msg': '创建成功'
        }

        return JsonResponse(python_dict)


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
        # 4.更新数据
        project_obj.name = python_data.get("name")
        project_obj.leader = python_data.get("leader")
        project_obj.is_execute = python_data.get("is_execute")
        project_obj.desc = python_data.get("desc")
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




