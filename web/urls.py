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

    re_path(r'shop/shoping-cart', views.cart_detail, name='shoping-cart'),
    
    re_path(r'shop/add/(?P<product_id>[-\w]+)/$', views.cart_add, name='cart_add'),
    re_path(r'shop/remove/(?P<product_id>[-\w]+)/$', views.cart_remove, name='cart_remove'),
 
    re_path(r'list/bycat/(?P<category_id>[-\w]+)/$',
        views.product_list,
        name='product_list_by_category'),   

    re_path(r'shop/list/product/(?P<id>\d+)/$',
        views.product_detail, name='product_detail'),  
 
    re_path(r'list/', views.product_list,name='product_list'),




]
