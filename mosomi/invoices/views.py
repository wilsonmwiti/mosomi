from django.contrib import messages
from django.shortcuts import render, redirect
from invoices.models import *


def invoice_clients(request):
    clients = Client.objects.all()
    context = {
        'clients': clients
    }
    return render(request, 'invoices/invoice_clients.html', context)


def create_client(request):
    if request.method == 'POST':
        customer_number = ''
        last_client = Client.objects.all().order_by('id').last()
        if not last_client:
            customer_number = 'RB-100'
        else:
            cn = last_client.client_number
            cn_int = int(cn.split('RB-')[-1])
            new_cn_int = cn_int + 1
            new_cn = f"RB-{new_cn_int}"
            customer_number = new_cn
        Client.objects.create(
            company_name=request.POST['company_name'],
            phone_number=request.POST['phone_number'],
            client_number=customer_number,
            kra_pin=request.POST['kra_pin'],
            address=request.POST['address'],
            location=request.POST['location']
        )
        messages.success(request, 'Client Added Successfully')
        return redirect('Invoices:invoice_clients')
    return render(request, 'invoices/create_client.html')


def edit_client(request, client_id):
    client = Client.objects.get(id=client_id)
    if request.method == 'POST':
        client.company_name = request.POST['company_name']
        client.phone_number = request.POST['phone_number']
        client.kra_pin = request.POST['kra_pin']
        client.address = request.POST['address'],
        client.location = request.POST['location']
        client.save()
        messages.success(request, 'Client Edited Successfully')
        return redirect('Invoices:invoice_clients')
    context = {
        'client': client
    }
    return render(request, 'invoices/edit_client.html', context)


def client_invoices(request, client_id):
    client = Client.objects.get(id=client_id)
    invoices = Invoice.objects.filter(client=client)

    context = {
        'client': client,
        'invoices': invoices
    }
    return render(request, 'invoices/client_invoices.html', context)


def create_invoice(request, client_id):
    client = Client.objects.get(id=client_id)

    if request.method == 'POST':
        invoice_number = ''
        last_invoice = Invoice.objects.all().order_by('id').last()
        if not last_invoice:
            invoice_number = 'RBLTD-100'
        else:
            cn = last_invoice.invoice_number
            cn_int = int(cn.split('RBLTD-')[-1])
            new_cn_int = cn_int + 1
            new_cn = f"RBLTD-{new_cn_int}"
            invoice_number = new_cn

        invoice = Invoice.objects.create(
            client=client,
            invoice_date=request.POST['invoice_date'],
            discount=request.POST['discount'],
            invoice_number=invoice_number,
            vat=int(request.POST['vat'])
        )
        messages.success(request, 'Invoice Creation Success');
        return redirect('Invoices:invoice_services', invoice.id)
    context = {
        'client': client
    }
    return render(request, 'invoices/create_invoice.html', context)


def edit_invoice(request, invoice_id):
    invoice = Invoice.objects.filter(id=invoice_id).first()
    if request.method == 'POST':
        invoice_date = request.POST['invoice_date']
        discount = request.POST['discount']
        invoice.invoice_date = invoice_date
        invoice.discount = discount
        invoice.vat = request.POST['vat']
        invoice.save()
        messages.success(request, 'Invoice Editing Success')
        return redirect('Invoices:client_invoices', invoice.client_id)
    else:
        context = {
            'invoice': invoice
        }
        return render(request, 'invoices/edit_invoice.html', context)


def invoice_services(request, invoice_id):
    invoice = Invoice.objects.get(id=invoice_id)
    services = Service.objects.filter(invoice=invoice)

    context = {
        'invoice': invoice,
        'services': services
    }
    return render(request, 'invoices/invoice_services.html', context)


def add_invoice_services(request, invoice_id):
    invoice = Invoice.objects.get(id=invoice_id)
    if request.method == 'POST':
        service, created = Service.objects.update_or_create(
            invoice_id=invoice_id,
            service=request.POST['service'],
            unit_price=request.POST['unit_price'],
            quantity=request.POST['quantity']
        )
        messages.success(request, 'Invoice Service Addition Success')
        return redirect('Invoices:invoice_services', invoice.id)
    context = {
        'invoice': invoice
    }
    return render(request, 'invoices/add_invoice_service.html', context)


def edit_invoice_service(request, service_id):
    service = Service.objects.filter(id=service_id).first()
    if request.method == 'POST':
        service_name = request.POST['service_name']
        unit_price = request.POST['unit_price']
        quantity = request.POST['quantity']

        service.service = service_name
        service.unit_price = unit_price
        service.quantity = quantity
        service.save()
        messages.success(request, 'Invoice Service Editing Successful')
        return redirect('Invoices:invoice_services', service.invoice_id)
    else:
        context = {
            'service': service
        }
        return render(request, 'invoices/edit_invoice_service.html', context)


def invoice_preview(request, invoice_id):
    invoice = Invoice.objects.get(id=invoice_id)
    services = Service.objects.filter(invoice=invoice)
    client = Client.objects.get(id=invoice.client.id)
    total_amount = 0
    for service in services:
        total_amount += (float(service.unit_price) * float(service.quantity))
    discount = 0
    if invoice.discount:
        discount = total_amount * (float(invoice.discount)) / 100
    else:
        discount = 0
    new_total = total_amount - discount
    sub_total = new_total
    vat = new_total * invoice.vat/100
    new_total += vat
    context = {
        'invoice': invoice,
        'services': services,
        'total': total_amount,
        'new_total': new_total,
        'sub_total': sub_total,
        'discount': discount,
        'vat': vat,
        'client': client
    }
    return render(request, 'invoices/invoice_preview.html', context)


def invoice_payments(request, invoice_id):
    invoice = Invoice.objects.filter(id=invoice_id).first()
    payments = Payments.objects.filter(invoice=invoice, invoice__client_id=invoice.client_id)

    context = {
        'payments': payments,
        'invoice': invoice
    }
    return render(request, 'invoices/invoice_payments.html', context)


def add_payment(request, invoice_id):
    invoice = Invoice.objects.filter(id=invoice_id).first()

    if request.method == 'POST':
        amount = request.POST['amount']
        services = Service.objects.filter(invoice=invoice)
        invoice_total = 0.0
        for service in services:
            invoice_total += (float(service.unit_price) * float(service.quantity))
        discount = invoice_total * float(float(invoice.discount)/100)
        new_total = invoice_total - discount
        vat = new_total * invoice.vat / 100
        new_total += vat

        payed_amount = 0
        for payment in Payments.objects.filter(invoice=invoice):
            payed_amount += float(payment.amount)
        if float(amount) + payed_amount == new_total:
            Payments.objects.create(
                invoice=invoice,
                amount=amount,
            )
            invoice.status_complete = True
            invoice.save()
            messages.success(request, 'Invoice Payment Complete')
        else:
            Payments.objects.create(
                invoice=invoice,
                amount=amount,
            )
            messages.success(request, 'Partial Payment Added Successfully')
            return redirect('Invoices:invoice_payments', invoice.id)
    context = {
        'invoice': invoice
    }
    return render(request, 'invoices/add_invoice_payment.html', context)


def mark_invoice_as_payed(request, invoice_id):
    invoice = Invoice.objects.filter(id=invoice_id).first()
    invoice.status_complete = True
    invoice.save()

    services = Service.objects.filter(invoice=invoice)
    invoice_total = 0.0
    for service in services:
        invoice_total += (float(service.unit_price) * float(service.quantity))
    discount = 0
    if invoice.discount:
        discount = invoice_total * float(float(invoice.discount)/100)
    else:
        discount = 0
    new_total = invoice_total - discount
    vat = new_total * 16 / 100
    new_total += vat

    payable_total = 0
    payments = Payments.objects.filter(invoice_id=invoice.id)
    if payments is not None:
        for payment in payments:
            payable_total =+ float(payment.amount)

    new_total = new_total - payable_total

    Payments.objects.create(
        invoice=invoice,
        amount=new_total,
    )
    return redirect('Invoices:invoice_payments', invoice.id)


def delete_service(request, service_id):
    service = Service.objects.get(id=service_id)
    invoice_id = service.invoice.id
    service.delete()
    messages.success(request, 'Service Deleted Successfully')
    return redirect('Invoices:invoice_services', invoice_id)


def delete_invoice(request, invoice_id):
    invoice = Invoice.objects.get(id=invoice_id)
    client_id = invoice.client.id
    invoice.delete()
    messages.success(request, 'Invoice Deleted Successfully')
    return redirect('Invoices:client_invoices', client_id)
