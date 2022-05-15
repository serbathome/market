import django
from django.conf import settings
from django.db import models


# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    province = models.CharField(max_length=16, blank=False)
    city = models.CharField(max_length=16, blank=False)
    zip = models.CharField(max_length=16, blank=False)
    address = models.CharField(max_length=64, blank=False)
    isFarmer = models.BooleanField(default=False, blank=False)
    wantPromoEmails = models.BooleanField(default=False, blank=False)
    wantMarketingEmails = models.BooleanField(default=False, blank=False)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} aka {self.user.username} ({self.user.email})"
