from django.db import models

# Create your models here.
from django.utils import timezone

from sms.models import Customer


class Mpesa(models.Model):
    first_name = models.CharField(max_length=250)
    last_name = models.CharField(max_length=250)
    description = models.CharField(max_length=250)
    phone_number = models.CharField(max_length=250)
    amount = models.CharField(max_length=250)
    reference = models.CharField(max_length=250)
    email = models.CharField(max_length=250)
    type = models.CharField(max_length=250)
    account_number = models.IntegerField(null=True)
    customer = models.ForeignKey(Customer, null=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(null=True)
    organization_balance = models.CharField(max_length=250, null=True)