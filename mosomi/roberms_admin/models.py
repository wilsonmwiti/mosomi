from django.db import models
from sms.models import SalesPerson


class Company(models.Model):
    name = models.CharField(max_length=250)
    phone_number = models.CharField(max_length=200)
    contact_person = models.CharField(max_length=250)
    email = models.EmailField(max_length=250)
    sales_person = models.ForeignKey(SalesPerson, on_delete=models.CASCADE)
    location = models.CharField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Appointment(models.Model):
    description = models.TextField()
    date_visited = models.DateTimeField()
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    status_visited = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


