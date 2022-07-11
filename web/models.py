from pyexpat import model
import django
from django.conf import settings
from django.db import models
from django.urls import reverse


# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    businessName = models.CharField(max_length=32, blank=False, default="N/A")
    province = models.CharField(max_length=16, blank=False)
    city = models.CharField(max_length=16, blank=False)
    zip = models.CharField(max_length=16, blank=False)
    address = models.CharField(max_length=64, blank=False)
    isFarmer = models.BooleanField(default=False, blank=False)
    wantPromoEmails = models.BooleanField(default=False, blank=False)
    wantMarketingEmails = models.BooleanField(default=False, blank=False)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} aka {self.user.username} ({self.user.email})"


MEASURE_CHOICES = (
    ("Gr", "Gr"),
    ("Kg", "Kg"),
    ("Btl", "Btl")
)


class ProductCategory(models.Model):
    CategoryName = models.CharField(max_length=200)

    def __str__(self):
        return f'{self.CategoryName}'

    def get_absolute_url(self):
        #    print('absolute_url_ProductCategories')
     #   print(self)
      #  print(self.id)
        return reverse('product_list_by_category',
                       args=[self.id])


class Product(models.Model):
    CategoryID = models.ForeignKey(
        'ProductCategory', on_delete=models.CASCADE)
    ProductName = models.CharField(max_length=200)
    Measure = models.CharField(
        max_length=3, choices=MEASURE_CHOICES, default='GR')
    Price = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    Picture = models.CharField(
        blank=False, default='/static/shop/img/product/product-1.jpg', max_length=200)

    def __str__(self):
        return f'{self.ProductName}'

    def get_absolute_url(self):
        return reverse('product_detail',
                       args=[self.id])


class Order(models.Model):
    product = models.OneToOneField(to=Product, on_delete=models.CASCADE)
    amount = models.IntegerField(blank=False, default=0)

    def __str__(self):
        return f"{self.product} : {self.amount}"
