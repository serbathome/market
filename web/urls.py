from django.urls import path, re_path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('api/get_categories', views.get_categories, name='get_categories'),
    path('api/get_products', views.get_products, name='get_products'),
    re_path(r'^$', views.cart_detail, name='cart_detail'),
    re_path(r'add/(?P<product_id>[-\w]+)/$', views.cart_add, name='cart_add'),
    re_path(r'remove/(?P<product_id>[-\w]+)/$', views.cart_remove, name='cart_remove'),
]
