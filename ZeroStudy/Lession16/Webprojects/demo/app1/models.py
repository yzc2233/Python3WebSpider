from django.db import models

# Create your models here.
class CreateUpdate(models.Model):#创建抽象数据模型，同样要继承与models.Model
    #创建时间，使用models.DateTimeField
    create_at = models.DateTimeField(auto_now_add=True)
    #修改时间，使用models.DateTimeField
    update_at = models.DateTimeField(auto_now_add=True)

    class Meta:#元数据，除了字段以外的所有属性
        #设置model为抽象类。指定该表不应该在数据库创建
        abstract = True



class Person(CreateUpdate):#继承CreateUpdate基类
    #第一个字段使用models.CharField类型
    first_name = models.CharField(max_length=30)
    #第二个字段使用models.CharField类型
    last_name = models.CharField(max_length=30)

class Order(CreateUpdate):
    order_id = models.CharField(max_length=30,db_index=True)
    order_desc = models.CharField(max_length=120)














