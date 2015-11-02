#coding:utf-8
from django.db import models
from django.contrib.auth.models import User

class Base(models.Model):
    create_user = models.ForeignKey(User,related_name='creator')
    create_time = models.DateTimeField(auto_now_add=True)
    write_user = models.ForeignKey(User,null=True)
    write_time = models.DateTimeField(auto_now=True)
    description = models.CharField(max_length=200,null=True)
    class Meta:
        abstract=True
        ordering = ['-create_time']

class Company(Base):
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=200,null=True)
    website = models.URLField(null=True)
    inside_description = models.TextField(null=True)#内部备注
    is_customer =models.BooleanField(default=False) #是否为客户
    is_supplier = models.BooleanField(default=False)#是否为供应商
    is_available =models.BooleanField(default=False)#是否可用

