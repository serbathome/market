from django.contrib import admin

from .models import ProductCategory, Profile, Product

# Register your models here.

admin.site.register(Profile)
admin.site.register(ProductCategory)
admin.site.register(Product)
