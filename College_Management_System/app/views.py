from django.shortcuts import render

# Create your views here.

def loginpage(request):
    return render(request, 'login.html')

def home(request):
    return render(request,'index.html')

