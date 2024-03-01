from django.shortcuts import render

# Create your views here.

def dashboard(request):
    return render(request,'base.html')

def login(request):
    return render(request,'login.html')


def signup(request):
    return render(request,'signup.html')


def table(request):
    return render(request,'table.html')