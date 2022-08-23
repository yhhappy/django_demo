from rest_framework import serializers

from interfaces.models import Interfaces

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
    4.默认定义哪些字段，那么哪些字段就会返回前端，同时也必须得输入（前端需要传递）
    5.常用的序列化器字段类型
        IntegerField -> int
        CharField -> str
        BooleanField -> bool
        DateTimeField -> datetime
    6.可以在序列化器字段中指定不同的选项
        label和help_text，与模型类中的verbose_name和help_text参数一样
        IntegerField，可以使用max_value指定最大值，min_value指定最小值
        CharField，可以使用max_length指定最大长度，min_length指定最小长度
    7.定义的序列化器字段中，required默认为True，说明默认定义的字段必须得输入和输出
    8.如果在序列化器字段中，设置required为False，那么前端用户可以不传递该字段（校验时会忽略该字段，所以不会报错）
    9.如果未定义模型类中的某个字段，那么该字段不会输入，也不会输出
    10.前端必须的输入（反序列化输入）name（必须得校验），但是不会需要输出（序列化器输出）？
        如果某个参数指定了write_only=True，那么该字段仅仅只输入（反序列化输入，做数据校验），不会输出（序列化器输出），默认write_only为False
    11.前端可以不用传递，但是后端需要输出？
        如果某个参数指定了read_only=True，那么该字段仅仅只输出（序列化输出），不会输入（反序列化输入，做数据校验），默认read_only为False
    12.在序列化器类中定义的字段，默认allow_null=False，该字段不允许传递null值
        如果指定allow_null=True，那么该字段允许传递null
    13.在序列化器类中定义CharField字段，默认allow_blank=False，该字段不允许传递空字符串
        如果指定allow_blank=True，那么该字段允许传递空字符串
    14.在序列化器类中定义的字段，可以使用default参数来指定默认值，如果指定了default参数，那么前端用户可以不用传递，
        会将default指定的值作为入参
    """
    # id = serializers.IntegerField(label="项目id", help_text="项目id", max_value=1000, min_value=1)
    # 可以在任意序列化器字段上使用error_messages来自定义错误提示信息，使用校验项名作为key，把具体错误信息作为value
    name = serializers.CharField(label="项目名称", help_text="项目名称", max_length=20, min_length=5,
                                 error_messages={
                                     'min_length': '项目名称不能少于5位',
                                     'max_length': '项目名称不能超过20位'
                                 })
    leader = serializers.CharField(required=False, label="项目负责人", help_text="项目负责人", allow_null=True, default='默认')
    is_execute = serializers.BooleanField()
    # DatetimeFeild可以使用format参数指定格式化字符串
    update_time = serializers.DateTimeField(label='更新时间', help_text='更新时间', format='%Y年%m月%d日 %H:%M:%S',
                                            error_messages={'required': '该字段为必传参数'})
    """
    一、关联字段
    1.可以定义PrimaryKeyRelatedField来获取关联表的外键值
    2.如果通过父表获取从表数据，默认需要使用从表类名小写_set作为序列化器类中的关联字段名称
    3.如果在定义模型类的外键字段时，指定了related_name参数，那么会把related_name参数名作为序列化器类中的关联字段
    4.PrimaryKeyRelatedField字段，要么指定read_only=True，要么指定queryset参数，否则会报错
    5.如果指定了read_only=True，那么该字段仅序列化输出
    6.如果指定了queryset参数(关联表的查询集对象)，用于对参数进行校验
    7.如果关联字段有多个值，那么必须添加many=True，一般父表获取从表数据时，关联字段需要指定
    """
    # inter = serializers.PrimaryKeyRelatedField(label='项目所属接口id', help_text='项目所属接口id',
    #                                            many=True, queryset=Interfaces.objects.all(), write_only=True)
    """
    1.使用StringRelatedField字段，将关联字段模型类中的__str__方法的返回值作为该字段的值
    2.StringRelatedField字段默认添加了read_only=True，该字段仅序列化输出
    """
    # inter = serializers.StringRelatedField(many=True)
    """
    1.使用SlugRelatedField字段，将关联字段模型类中的某个字段，作为该字段的值
    2.如果指定了read_only=True，那么该字段仅序列化输出
    3.如果该字段需要进行反序列化输入，那么必须得指定queryset参数，同时关联字段必须有唯一约束
    """
    inter = serializers.SlugRelatedField(slug_field='name', many=True, queryset=Interfaces.objects.all())

