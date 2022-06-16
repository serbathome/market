from django.http import JsonResponse
from django.shortcuts import render

from web.models import ProductCategory, Product

# Create your views here.


def categories(request):
    categories = []
    for category in ProductCategory.objects.all():
        categories.append(category.CategoryName)
    return JsonResponse(categories, safe=False)


def products(request):
    products = []
    for product in Product.objects.all():
        products.append({
            'CategoryID': product.CategoryID.CategoryName,
            'ProductName': product.ProductName,
            'Measure': product.Measure,
            'Price': product.Price
        })
    return JsonResponse(products, safe=False)
