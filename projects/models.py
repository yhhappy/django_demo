from django.db import models
from utils.base_model import BaseModel


class Animal(models.Model):
    """
    1) 一般在子应用models.py中定义模型类（相当于数据库中的一张表）
    2) 必须继承Model或者Model子类
    3) 在模型类中定义属性（必须得为Field子类）相当于数据表中字段
    4) CharField ---> varchar
       IntegerField ---> integer
       BooleanField ---> bool
    5) 在migrations里，存放迁移脚本：
        python manage.py makemigrations 子应用名（如果不指定子应用名，会把所有子应用生成迁移脚本）
    6) 查询迁移脚本生成的SQL语句：python manage.py sqlmigrate 子应用名 迁移脚本名（无需加.py）
    7) 生成的数据表名称默认为：子应用名_模型类名小写
    8) 默认会自动创建一个名为id的自增主键
    """
    name = models.CharField(max_length=50)
    age = models.IntegerField()
    gender = models.BooleanField()


class Projects(BaseModel):
    """
    a. CharField类型必须指定max_length参数（该字段的最大字节数）
    b. 如果需要给一个字段添加唯一约束，unique=True(默认为False)
    c. 使用default指定默认值（如果指定默认值后，在创建记录时，该字段传递会使用默认值）
    d. null=True指定前端创建数据时，可以指定该字段为null，默认为null=False，DRF进行反序列化器输入时才有效
    e. blank=True指定前端创建数据时，可以指定该字段为空字符串，默认为blank=False，DRF进行反序列化器输入时才有效
    f. 在DateTimeField、DateField等字段中，指定auto_now_add=True，在创建一条记录时，会自动创建记录时的时间作为该字段的值，后续再更新数据时，就不再修改
    g. 在DateTimeField、DateField等字段中，指定auto_now=True，在更新一条记录时，会自动更新记录时的时间作为该字段的值
    h. 可以在任意一个模型类中创建Meta内部类，用于修改数据库的元数据信息
    i. 在一个模型类中仅仅只能为一个字段指定primary_key=True，一旦在模型类中的某个字段上指定了primary_key=True，那么ORM框架就不会自动创建
    名称为id的主键
    """
    # ids = models.IntegerField(primary_key=True, verbose_name='项目主键', help_text='项目主键')
    name = models.CharField(max_length=20, verbose_name='项目名称', help_text='项目名称', unique=True)
    leader = models.CharField(max_length=10, verbose_name='项目负责人', help_text='项目负责人')
    is_execute = models.BooleanField(verbose_name='是否启动项目', help_text='是否启动项目', default=True)
    desc = models.TextField(verbose_name='项目描述信息', help_text='项目描述信息', null=True, blank=True, default='')
    # create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间', help_text='创建时间')
    # update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间', help_text='更新时间')

    class Meta:
        # db_table指定创建的数据表名称
        db_table = 'tb_projects'
        # 为当前数据表设置中文描述信息
        verbose_name = '项目表'
        verbose_name_plural = '项目表'
        ordering = ['id']

    def __str__(self):
        return f"Projects({self.name})"
