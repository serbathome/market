from django.http import JsonResponse
from django.shortcuts import render

from web.models import ProductCategory

# Create your views here.


def categories(request):
    categories = []
    for category in ProductCategory.objects.all():
        categories.append(category.CategoryName)
    return JsonResponse(categories, safe=False)
