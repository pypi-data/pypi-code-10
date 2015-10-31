from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class ProductCategory(models.Model):
    create_time = models.DateTimeField(auto_now_add=True)
    create_uid = models.ForeignKey(User)
    write_time = models.DateTimeField(auto_now=True)
    write_uid =models.ForeignKey(User,related_name='category_write_user_id',null=True)
    name = models.CharField(max_length=20)
    class Meta:
        ordering=["-create_time"]
    def __unicode__(self):
        return self.name

class Product(models.Model):
    create_time = models.DateTimeField(auto_now_add=True)
    create_uid = models.ForeignKey(User)
    write_time = models.DateTimeField(auto_now=True)
    write_uid =models.ForeignKey(User,related_name='product_write_user_id',null=True)
    category = models.ForeignKey(ProductCategory,related_name='products')
    name = models.CharField(max_length=20)
    description = models.CharField(max_length=200)
    price = models.IntegerField()
    class Meta:
        ordering=["-create_time"]

class Order(models.Model):
    create_time = models.DateTimeField(auto_now_add=True)
    create_uid = models.ForeignKey(User)
    write_time = models.DateTimeField(auto_now=True)
    write_uid =models.ForeignKey(User,related_name='write_user',null=True)
    state = models.CharField(max_length=30)
    total = models.IntegerField()
    class Meta:
        ordering=['-create_time']

class Order_line(models.Model):
    create_time = models.DateTimeField(auto_now_add=True)
    create_uid = models.ForeignKey(User)
    write_time = models.DateTimeField(auto_now=True)
    write_uid =models.ForeignKey(User,related_name='line_write_user',null=True)
    order = models.ForeignKey(Order,related_name='order_set')
    state = models.CharField(max_length=30)
    qty = models.IntegerField()
    price = models.IntegerField()
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    class Meta:
        ordering=['-create_time']

class Cashmove(models.Model):
    create_time = models.DateTimeField(auto_now_add=True)
    create_uid = models.ForeignKey(User,related_name='cashmove_create_user')
    write_time = models.DateTimeField(auto_now=True)
    write_uid =models.ForeignKey(User,related_name='cashmove_wirte_user',null=True)
    user = models.ForeignKey(User)
    order_line = models.ForeignKey(Order_line,null=True)
    amount = models.IntegerField()
    state=models.CharField(max_length=50)
    description=models.CharField(max_length=200,null=True)
    class Meta:
        ordering=['-create_time']

