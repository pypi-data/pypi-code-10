from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
# Create your views here.
def login_html(request):
    return render(request,'usercenter/usercenter_login.html')

def register_html(request):
    return  render(request,'usercenter/usercenter_register.html')

@login_required
def changepwd_html(request):
    return  render(request,'usercenter/usercenter_changepwd.html')

@login_required
def index(request):
    return render(request,'bases/base_with_nav.html')

@login_required
def logout_user(request):
    logout(request)
    return login_html(request)