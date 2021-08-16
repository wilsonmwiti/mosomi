import urllib
from random import randrange

from django import template
import json

from invoices.models import Service, Invoice
from school.models import *
from sms.models import *
from sms.utils import calculate_message_cost

register = template.Library()


@register.filter(name='commission_count')
def commission_count(sales_person_id):
    sales_person = SalesPerson.objects.filter(user_ptr_id=sales_person_id).first()
    if sales_person is not None:
        sales = Sale.objects.filter(sales_person_id=sales_person.id)
        customer_ids = []
        for sale in sales:
            customer_ids.append(sale.customer_id)
        top_ups = ManagerTopUp.objects.filter(user_id__in=customer_ids, commission_paid=False)
        commission = 0
        for top_up in top_ups:
            if sales_person.commission:
                commission_p = sales_person.commission/100

                if top_up.amount != 'O' and top_up.amount != 'o':
                    commission += float(top_up.amount) * commission_p
            else:
                commission += float(top_up.amount) * 0.2
        return commission


@register.filter(name='get_email')
def get_email(user_id):
    user = Customer.objects.filter(id=user_id).first()
    return user.username

