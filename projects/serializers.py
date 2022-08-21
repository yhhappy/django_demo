from rest_framework import serializers

"""
一、序列化器
a.如果需要使用DRF框架来实现序列化、反序列化、数据操作，在子应用中创建serializers.py文件
b.文件名推荐命名为serializers.py
"""


class ProjectSerializer(serializers.Serializer):
    """
    定义序列化器
    1.必须得继承Serializer类或者Serialiazer子类
    2.定义的序列化器类中，字段名要与模型类中的字段名保持一致
    3.定义的序列化器类的字段（类属性）为Field子类
    4.默认定义哪些字段，那么哪些字段就会返回前端
    5.常用的序列化器字段类型
        IntegerField -> int
        CharField -> str
        BooleanField -> bool
        DateTimeField -> datetime
    6.可以在序列化器字段中指定不同的选项
        label和help_text，与模型类中的verbose_name和help_text参数一样
        IntegerField，可以使用max_value指定最大值，min_value指定最小值
        CharField，可以使用max_length指定最大长度，min_length指定最小长度
    """
    id = serializers.IntegerField(label="项目id", help_text="项目id", max_value=1000, min_value=1)
    name = serializers.CharField(label="项目名称", help_text="项目名称", max_length=20, min_length=5)
    leader = serializers.CharField()
    is_execute = serializers.BooleanField()
    update_time = serializers.DateTimeField()
