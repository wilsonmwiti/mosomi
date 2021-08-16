from django.db import models
from sms.models import Customer


class DeliveryUrl(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    delivery_url = models.CharField(max_length=250)
