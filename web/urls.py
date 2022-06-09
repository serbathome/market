from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('api/get_categories', views.get_categories, name='get_categories'),
    path('api/get_products', views.get_products, name='get_products'),
]
