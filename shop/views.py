from django.http import HttpResponse
from django.shortcuts import render
from web.models import Product, ProductCategory, Order

# Create your views here.


def index(request):
    return render(request, 'shop/index.html')


def blog(request):
    return render(request, 'shop/blog.html')


def grid(request):
    return render(request, 'shop/example.html')


def cart(request):
    return render(request, 'shop/shoping-cart.html')


def orders(request):
    orders = Order.objects.all()
    cart = []
    for order in orders:
        cart.append(
            {
                'product': order.product,
                'quantity': order.amount,
                'total': order.product.Price * order.amount
            }
        )
        print(order)
    return render(request, 'shop/shoping-cart.html', {'cart': cart})
