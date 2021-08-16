from django.contrib import admin

# Register your models here.
from sms.models import *

admin.site.register(Customer)
admin.site.register(Outgoing)
admin.site.register(Outgoing1)
admin.site.register(Outgoing2)
admin.site.register(OutgoingDone)
admin.site.register(Group)
admin.site.register(Contact)
admin.site.register(UserTopUp)
admin.site.register(MpesaPayments)
admin.site.register(Sms_TopUp)
admin.site.register(CustomerSubAccounts)
# admin.site.register(Manager)
# admin.site.register(SalesPerson)

