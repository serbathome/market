from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.


def index(request):
    return render(request, 'shop/index.html')


def blog(request):
    return render(request, 'shop/blog.html')
