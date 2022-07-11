from django.urls import path, re_path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('blog/', views.blog, name='blog'),
    path('grid/', views.grid, name='grid'),
    path('cart/', views.cart, name='cart'),
    path('orders/', views.orders, name='orders'),
]
