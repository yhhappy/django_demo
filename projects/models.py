from django.db import models


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
