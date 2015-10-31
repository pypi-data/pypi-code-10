from rest_framework import serializers
from lunchapp.models import Product,ProductCategory,Order,Order_line,Cashmove

class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = ('id','create_time','create_uid','write_time','write_uid','name')

class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.StringRelatedField(source='category')
    class Meta:
        model = Product
        fields = ('id','create_time','create_uid','write_time','write_uid','name','description','price','category','category_name')

class Order_lineSerializer(serializers.ModelSerializer):
    creator = serializers.StringRelatedField(source='create_uid')
    class Meta:
        model = Order_line
        fields = ('id','create_time','create_uid','write_time','write_uid','order','state','qty','price','name','description','creator')

class OrderSerializer(serializers.ModelSerializer):
    order_set = Order_lineSerializer(many=True,read_only=True)
    class Meta:
        model = Order
        fields = ('id','create_time','create_uid','write_time','write_uid','state','total','order_set')


class CashmoveSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    create_uid = serializers.StringRelatedField()
    class Meta:
        model = Cashmove
        fields = ('id','create_time','create_uid','write_time','write_uid','user','order_line','amount','state','description')
