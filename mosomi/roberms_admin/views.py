from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.core.mail import EmailMultiAlternatives
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.crypto import get_random_string
from invoices.models import Client
from roberms_admin.models import Company, Appointment
from sms.models import *
from sms.utils import SDP


def dashboard(request):
    sales_people = SalesPerson.objects.all()
    clients = Customer.objects.all()
    text_messages = Outgoing.objects.all()
    context = {
        'sales_people': sales_people,
        'clients': clients,
        'sales_people_count': sales_people.count(),
        'clients_count': clients.count()
    }
    return render(request, 'roberms_admin/dashboard.html', context)


def clients(request):
    clients = Customer.objects.filter(is_active=True)
    context = {
        'clients': clients
    }
    return render(request, 'roberms_admin/clients.html', context)


def client_edit(request, client_id):
    customer = Customer.objects.filter(id=client_id).first()
    if request.method == 'POST':
        sender_name = request.POST['sender_name']
        sender_id = request.POST['sender_id']
        access_code = request.POST['access_code']
        customer.service_id = sender_id
        customer.access_code = access_code
        customer.sender_name = sender_name
        customer.save()
        messages.success(request, f'customer {customer.first_name} {customer.last_name} service id and access code updated successfully')
        return redirect('roberms_admin:clients')
    context = {
        'customer': customer
    }
    return render(request, 'roberms_admin/customer_sender_id.html', context)


def sales_people(request):
    sales_people = SalesPerson.objects.all()
    context = {
        'sales_people': sales_people
    }
    return render(request, 'roberms_admin/sales_people.html', context)


def activate_deactivate_sales_person(request, person_id):
    sales_person = SalesPerson.objects.get(id=person_id)
    if sales_person.is_active:
        sales_person.is_active = False
        sales_person.save()
        messages.success(request, 'Sales person deactivated succesfully')
        return redirect('roberms_admin:sales_people')
    else:
        sales_person.is_active = True
        sales_person.save()
        messages.success(request, 'Sales person Activated Successfully')
        return redirect('roberms_admin:sales_people')


def add_sales_person(request):
    if request.method == 'POST':
        email = request.POST['email']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        password = request.POST['password']
        commission = request.POST['commission']
        # password = get_random_string(length=10)
        phone_number = request.POST['phone_number']

        if User.objects.filter(email=email).count() < 1:
            SalesPerson.objects.create(
                username=email,
                email=email,
                first_name=first_name,
                last_name=last_name,
                password=make_password(password),
                phone_number=phone_number,
                commission=commission,
            )
            print(password)
            messages.success(request, 'Sales Person Added Successfully')
            return redirect("roberms_admin:sales_people")
        else:
            messages.error(request, 'That email has already been registered to this system')
            return redirect("roberms_admin:add_sales_person")
    return render(request, 'roberms_admin/add_sales_person.html')


def delete_sales_person(request, person_id):
    sales_person = SalesPerson.objects.get(id=person_id)
    sales_person.delete()
    messages.success(request, 'Sales Person Deleted Successfully')
    return redirect('roberms_admin:sales_people')


def assign_client(request, sales_person_id):
    sales = Sale.objects.all()
    ids = []
    for sale in sales:
        ids.append(sale.customer_id)

    if request.method == 'POST':
        client_ids = request.POST.getlist('client_ids[]')
        for id in client_ids:
            print(id)
            Sale.objects.create(
                customer_id=id,
                sales_person_id=sales_person_id
            )
        messages.success(request, 'Clients Assigned Successfully')
        return redirect('roberms_admin:dashboard')
    clients = Customer.objects.exclude(id__in=ids)
    context = {
        'clients': clients,
        'sales_person_id': sales_person_id
    }
    return render(request, 'roberms_admin/assign_client.html', context)


def sales_person_clients(request, sales_person_id):
    sales = Sale.objects.filter(sales_person_id=sales_person_id)
    sales_person = SalesPerson.objects.filter(id=sales_person_id).first()
    client_ids = []
    for sale in sales:
        client_ids.append(sale.customer_id)
    clients = Customer.objects.filter(id__in=client_ids)
    context = {
        'clients': clients,
        'sales_person': sales_person
    }
    return render(request, 'roberms_admin/sales_person_clients.html', context)


def client_top_ups(request, client_id):
    top_ups = ManagerTopUp.objects.filter(user_id=client_id)
    context = {
        'top_ups': top_ups
    }
    return render(request, 'roberms_admin/client_top_ups.html', context)


def top_ups(request):
    client_top_ups = ManagerTopUp.objects.all()
    context = {
        'top_ups': client_top_ups
    }
    return render(request, 'roberms_admin/top_ups.html', context)


def add_client_credit(request):

    if request.method == 'POST':
        sms_count = request.POST['sms_count']
        amount = request.POST['amount']
        user_id = request.POST['customer']
        customer = Customer.objects.filter(id=user_id).first()
        customer.credit = customer.credit + float(sms_count)
        customer.save()
        ManagerTopUp.objects.create(
            sms_count=sms_count,
            amount=amount,
            user_id=user_id,
            timestamp=datetime.datetime.now()
        )
        messages.success(request, 'Credit Updated Successfully')
        return redirect('roberms_admin:top_ups')
    else:
        context = {
            'customers': Customer.objects.all()
        }
        return render(request, 'roberms_admin/add_top_up.html', context)


def mark_commission_paid(request, top_up_id):
    top_up = ManagerTopUp.objects.filter(id=top_up_id).first()
    if top_up is not None:
        client = top_up.user_id
        if top_up.commission_paid == True:
            messages.error(request, 'Commission Already Marked As Payed')
            return redirect("roberms_admin:client_top_ups", client)
        else:
            top_up.commission_paid = True
            top_up.save()
            messages.success(request, 'Commission Marked As Paid')
            return redirect("roberms_admin:client_top_ups", client)


def account_usage(request):
    top_ups = ManagerTopUp.objects.all()
    customers = Customer.objects.all()
    data = []
    # for customer in customers:
    #     data.append(customer.annotate(last_top_up=top_up for top_up in top_ups ))

    context = {
        'customers': customers
    }
    return render(request, 'roberms_admin/credit_usage.html', context)


def list_sales_people(request):
    people = SalesPerson.objects.all()
    context = {
        'people': people
    }
    return render(request, 'company/sales_people.html', context)


def sales_person_companies(request, sales_person_id):
    companies = Company.objects.filter(sales_person_id=sales_person_id)

    context = {
        'companies': companies
    }
    return render(request, 'company/company_list.html', context)


def company_appointments(request, company_id):
    appointments = Appointment.objects.filter(company_id=company_id)

    context = {
        'appointments': appointments
    }
    return render(request, 'company/appointments.html', context)


# def unapproved_clients(request):
#     clients = Customer.objects.filter(is_active=False)
#     context ={
#         'clients': clients
#     }
#     return render(request, 'roberms_admin/unapproved_clients.html', context)


# def activate_client(request, client_id):
#     client = Customer.objects.filter(is_active=False, id=client_id).first()
#     if client is not None:
#         password = get_random_string(length=8)
#         admin = Customer.objects.filter(id=1).first()
#         client.password = password
#         client.is_active = True
#         client.save()
#         invite_message = f"You have been added to Roberms LTD bulk sms platform. " \
#             f"Use the details below to sign in to you account" \
#             f" Email : {client.email}, Password : {password}"
#         sdp = SDP()
#         response = sdp.send_sms_customized(service_id=admin.service_id, recipients=[client.phone_number],
#                                            message=invite_message, sender_code='')
#         print(response.text)
#         messages.success(request, 'Client approval complete')
#         return redirect('roberms_admin:unapproved_clients')
#     else:
#         messages.error(request, 'Client Does Not Exist Or Has Already Been Approved')
#         return redirect('roberms_admin:unapproved_clients')


#dummy

def client_images(request):
    return render(request, 'dummy/show_images.html')