from django.db import models

# Create your models here.


class Client(models.Model):
    company_name = models.CharField(max_length=250)
    phone_number = models.CharField(max_length=250)
    client_number = models.CharField(max_length=250)
    address = models.CharField(max_length=250)
    location = models.CharField(max_length=250)
    kra_pin = models.CharField(max_length=250, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Client'
        verbose_name_plural = 'Clients'


class Invoice(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    invoice_date = models.CharField(max_length=250)
    invoice_number = models.CharField(max_length=250, null=True)
    discount = models.CharField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)
    status_complete = models.BooleanField(default=False)
    vat = models.IntegerField(default=16)

    class Meta:
        verbose_name = 'Invoice'
        verbose_name_plural = 'Invoices'


class Service(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    service = models.TextField()
    unit_price = models.CharField(max_length=250)
    quantity = models.CharField(max_length=250)


class Payments(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    amount = models.CharField(max_length=250)

    class Meta:
        verbose_name = 'Payment'
        verbose_name_plural = 'Payments'