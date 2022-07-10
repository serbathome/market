from django.urls import path, re_path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('blog/', views.blog, name='blog'),
    path('example/', views.example, name='example'),
   
]
