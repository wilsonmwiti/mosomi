import urllib
from random import randrange

from django import template
import json

from invoices.models import Service, Invoice
from sms.models import *
from sms.utils import calculate_message_cost

register = template.Library()


@register.filter(name='array_to_string')
def array_to_string(a_disctionary, option):
    output = []
    if option == 'keys':
        output = '["'
        output += '","'.join([str(x) for x in a_disctionary.keys()])
        output += '"]'
        # for x in a_disctionary.keys():
        #     output.append(x)
    elif option == 'values':
        output = '['
        output += ','.join([str(x) for x in a_disctionary.values()])
        output += ']'
        # output += ','.join([str(x) for x in a_disctionary.values()])
        # for x in a_disctionary.values():
        #     output.append(int(x))
    return output


@register.filter(name='get_track_code_participants')
def get_track_code_participants(track_code):
    return OutgoingDone.objects.filter(track_code=track_code).count()


@register.filter(name='customer_credit')
def customer_credit(user):
    customer = Customer.objects.filter(user_ptr_id=user.id).first()
    if customer is not None:
        return customer.credit
    else:
        return CustomerSubAccounts.objects.filter(user_ptr_id=user.id).first().owner.credit


@register.filter(name='get_date_sent')
def get_date_sent(track_code):
    date = OutgoingDone.objects.filter(track_code=track_code).first().sent_time
    return date


@register.filter(name='contacts_count')
def contacts_count(group):
    count = Contact.objects.filter(group=group).count()
    return count


@register.filter(name='credit_used')
def credit_used(track_code):
    messages = OutgoingDone.objects.filter(track_code=track_code)
    cost = 0
    for message in messages.iterator():
        cost += calculate_message_cost(message.text_message)
    return cost


@register.filter(name='get_business_name')
def get_business_name(user):
    # print(user.username)
    customer = Customer.objects.filter(user_ptr_id=user.id).first()
    if customer is not None:
        business_name = ''
        if customer.business_name == 'Business Name':
            business_name = user.email
        else:
            business_name = customer.business_name
        # print(business_name)
        return business_name
    else:
        customer = CustomerSubAccounts.objects.filter(user_ptr_id=user.id).first().owner
        business_name = ''
        if customer.business_name == 'Business Name':
            business_name = user.email
        else:
            business_name = customer.business_name
        # print(business_name)
        return business_name


@register.filter(name='get_services_amount')
def get_services_amount(service):
    amount = float(service.unit_price) * float(service.quantity)
    return amount


@register.filter(name='last_top_up_date')
def last_top_up_date(customer_id):
    date = ManagerTopUp.objects.filter(user_id=customer_id).last()
    if date is not None:
        t_date = date.timestamp.split(' ', 1)[0]
        return t_date


@register.filter(name='last_top_up_amount')
def last_top_up_amount(customer_id):
    amount = ManagerTopUp.objects.filter(user_id=customer_id).last()
    if amount is not None:
        return amount.amount


@register.filter(name='formatted_date')
def format_date(string):
    data = string.split(' ', 1)[0]
    return data