from django.contrib import admin

# Register your models here.
from invoices.models import Invoice, Client

admin.site.register(Invoice)
admin.site.register(Client)