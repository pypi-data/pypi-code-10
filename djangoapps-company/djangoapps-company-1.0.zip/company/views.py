#coding:utf-8
from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from company.models import Company
from django.contrib.auth.models import User
from company.serializers import CompanySerializer
from django.contrib.auth.decorators import login_required


class JSONResponse(HttpResponse):
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)

@login_required()
def index(request):
    return render(request,'company/index.html')
@login_required()
def company_list_template(request):
    return render(request,'company/companyList.html')
@login_required()
def company_edit_template(request):
    return render(request,'company/company_edit.html')
@login_required()
def company_change_template(request):
    return render(request,'company/company_change.html')


@csrf_exempt
def company_list(request):
    if request.method == 'GET':
        companies = Company.objects.all()
        serializer = CompanySerializer(companies,many=True)
        return JSONResponse(serializer.data,status=201)
    if request.method == 'POST':
        data = JSONParser().parse(request)
        data['create_user']=User.objects.get(username=request.user).id
        serializer = CompanySerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data,status=202)
        return JSONResponse(serializer.errors,status=400)

@csrf_exempt
def company_detail(request,company_id):
    try:
        company = Company.objects.get(id=company_id)
    except Company.DoesNotExist:
        return HttpResponse(status=404)
    if request.method == 'GET':
        serializer = CompanySerializer(company)
        return JSONResponse(serializer.data)
    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        data['write_user']=User.objects.get(username=request.user).id
        serializer = CompanySerializer(company, data=data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data)
        return JSONResponse(serializer.errors, status=400)
    elif request.method == 'DELETE':
        company.delete()
    return HttpResponse(status=204)



















