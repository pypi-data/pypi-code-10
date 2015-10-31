from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import View
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from lunchapp.models import ProductCategory,Product,Order,Order_line,Cashmove
from lunchapp.serializers import ProductCategorySerializer,ProductSerializer,Order_lineSerializer,OrderSerializer,CashmoveSerializer
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db.models import Q

class JSONResponse(HttpResponse):
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)
@login_required
def index(request):
        return render(request,'lunchapp/index.html',{})

class aaaa(View):
    def get(self,request):
        return render(request,'lunchapp/aaaa.html',{})


class product_category_add_template(View):
    def get(self,request):
        return render(request,'lunchapp/product_category_add_template.html',{})


class product_category_list_template(View):
    def get(self,request):
        return render(request,'lunchapp/product_category_list.html')

def product_list_template(request):
        return render(request,'lunchapp/product_list_template.html')


def product_category_detail_template(request):
    return render(request,'lunchapp/product_category_detail_template.html')

@login_required
@csrf_exempt
def product_category_add(request):
    user=User.objects.get(username=request.user)
    data = JSONParser().parse(request)
    data['create_uid']=user.id
    serializer = ProductCategorySerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return JSONResponse(serializer.data,status=201)

@login_required
def product_category_list(request):
    productcategories = ProductCategory.objects.all()
    serializer = ProductCategorySerializer(productcategories,many=True)
    return JSONResponse(serializer.data,status=201)

@login_required
def product_category_detail(request,category_id):
    if request.method == 'GET':
        product_category = ProductCategory.objects.get(id=category_id)
        serializer = ProductCategorySerializer(product_category)
        return JSONResponse(serializer.data,status=201)
    if request.method == 'POST':
        data = JSONParser().parse(request)
        product_category = ProductCategory.objects.get(id=category_id)
        product_category.name = data['name']
        product_category.write_uid=User.objects.get(username=request.user)
        product_category.save()
        serializer = ProductCategorySerializer(product_category)
        return JSONResponse(serializer.data,status=201)

@login_required
def product_category_delete(request,category_id):
    if request.method == 'GET':
        product_category = ProductCategory.objects.get(id=category_id)
        product_category.delete()
        return HttpResponse('ok',status=201)


def product_add_template(request):
        return render(request,'lunchapp/product_add_template.html',{})

def product_detail_template(request):
    return render(request,'lunchapp/product_detail_template.html')


def product_add(request):
    user = User.objects.get(username=request.user)
    data = JSONParser().parse(request)
    data['create_uid']=user.id
    serilaizer = ProductSerializer(data=data)
    if serilaizer.is_valid():
        serilaizer.save()
        return JSONResponse(serilaizer.data,status=200)
    return JSONResponse(serilaizer.errors)


def product_list(request):
    products=Product.objects.all()
    serializer = ProductSerializer(products,many=True)
    return JSONResponse(serializer.data,status=201)


def product_detail(request,product_id):
    if request.method == 'GET':
        product = Product.objects.get(id=product_id)
        serializer = ProductSerializer(product)
        return JSONResponse(serializer.data,status=201)
    if request.method == 'POST':
        data = JSONParser().parse(request)
        product = Product.objects.get(id=product_id)
        product.name = data['name']
        product.category = ProductCategory.objects.get(id=data['category']['id'])
        product.price = data['price']
        product.description = data['description']
        product.write_uid=User.objects.get(username=request.user)
        product.save()
        serializer = ProductSerializer(product)
        return JSONResponse(serializer.data,status=201)

def product_delete(request,product_id):
    if request.method == 'GET':
        product = Product.objects.get(id=product_id)
        product.delete()
        return HttpResponse('ok',status=201)

def order_add_template(request):
    return render(request,'lunchapp/order_add_template.html')

def account_charge_template(request):
    userlist = User.objects.all()

    return render(request,'lunchapp/account_charge_template.html',{'userlist':userlist})

def order_add(request):
    if request.method=='POST':
        total = 0
        boughtList = JSONParser().parse(request)
        order = Order()
        order.total=0
        order.state='new'
        order.create_uid=User.objects.get(username=request.user)
        order.save()
        for list in boughtList:
            list['state']='new'
            list['order']=order.id
            list['create_uid']=User.objects.get(username=request.user).id
            total+=list['qty']*list['price']
            serializer = Order_lineSerializer(data=list)
            if serializer.is_valid():
                serializer.save()
        order.total=total
        order.save()
        return JSONResponse('create success',status=200)

def orderlines_get(request):
    if request.method == 'GET':
        orderlines = Order_line.objects.filter(Q(state='new')|Q(state='confirmed'))
        serializer = Order_lineSerializer(orderlines,many=True)
        return JSONResponse(serializer.data,status=201)

def orders_get(reqeust):
    if reqeust.method == 'GET':
        orders = Order.objects.filter(create_uid=User.objects.get(username=reqeust.user))
        serializer = OrderSerializer(orders,many=True)
        return JSONResponse(serializer.data,status=201)

def my_orders_template(request):
    return render(request,'lunchapp/my_orders_template.html')

def order_line_cancel(request):
    if request.method == 'POST':
        order_line_data = JSONParser().parse(request)
        order_line = Order_line.objects.get(id=order_line_data['id'])
        if order_line.state=='new':
            order_line.state = 'canceled'
            order_line.save()
            serializer = Order_lineSerializer(order_line)
            return JSONResponse(serializer.data,status=201)
        else:
            return JSONResponse('already canceled',status=500)

def order_line_operation_template(request):
    return render(request,'lunchapp/order_line_operation_template.html')


def order_line_operate(request):
    if request.method == 'POST':
        order_line_data = JSONParser().parse(request)
        order_line = Order_line.objects.get(id=order_line_data['id'])
        if order_line.state=='new':
            order_line.state = 'confirmed'
            order_line.save()
            serializer = Order_lineSerializer(order_line)
            return JSONResponse(serializer.data,status=201)
        elif order_line.state=='confirmed':
            order_line.state = 'finished'
            order_line.save()
            cashmove=Cashmove()
            cashmove.create_uid = User.objects.get(username=request.user)
            cashmove.user = order_line.create_uid
            cashmove.order_line = order_line
            cashmove.amount =order_line.price * order_line.qty * -1
            cashmove.state = 'counsume'
            cashmove.description = order_line.name
            cashmove.save()
            serializer = Order_lineSerializer(order_line)
            return JSONResponse(serializer.data,status=201)

        else:
            return JSONResponse('already confirmed',status=500)

def all_orders_template(request):
    return render(request,'lunchapp/all_orders_template.html')

def all_orderlines_get(request):
    if request.method == 'GET':
        orderlines = Order_line.objects.all()
        serializer = Order_lineSerializer(orderlines,many=True)
        return JSONResponse(serializer.data,status=201)


def create_cashmove(request):
    if request.method=='POST':
        data = JSONParser().parse(request)
        cashmove = Cashmove()
        cashmove.create_uid = User.objects.get(username=request.user)
        cashmove.user = User.objects.get(id=data['user'])
        cashmove.amount = data['amount']
        cashmove.state = 'charge'
        cashmove.save()
        return JSONResponse('create cashmove success',status=201)

def all_cashmove_template(request):
    return render(request,'lunchapp/all_cashmove_template.html')

def all_cashmove(request):
    cashmoves = Cashmove.objects.all()
    serializer = CashmoveSerializer(cashmoves,many=True)
    return JSONResponse(serializer.data,status=201)

def my_cashmove_template(request):
    return render(request,'lunchapp/my_cashmove.html')

def my_cashmove(request):
    cashmoves = Cashmove.objects.filter(user=User.objects.get(username=request.user))
    serializer = CashmoveSerializer(cashmoves,many=True)
    return JSONResponse(serializer.data,status=201)