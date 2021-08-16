import random

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from celery.task import task
from shortcode.models import *


# @login_required
# def subs(request):
#     if request.user.id == 187:
#         subs = Subs40892.objects.all()
#         context = {
#             'subs': subs
#         }
#         return render(request, 'shortcode/subs.html', context)
#     else:
#         return redirect('sms:apps')


@login_required
def incoming_sms(request):
    if request.user.id == 187:
        sms = IncomingSmsSub.objects.all()
        context = {
            'sms': sms
        }
        return render(request, 'shortcode/incoming_sms.html', context)
    else:
        return redirect('sms:apps')


@login_required()
def simple_sms(request):
    if request.method == 'POST':
        message = request.POST['text_message']
        model = request.POST['model']
        short_code_sms_store.delay(message, model)
        messages.success(request, 'Message Queued For Sending')
        return redirect('ShortCode:reports')
    else:
        context = {
            'models': [Employer, Employee]
        }
        return render(request, 'shortcode/sms/simple_sms.html', context)


@task
def short_code_sms_store(message, model):
    if model == 'Employer':
        subs = Employer.objects.all()
        track_code = random.randint(300, 99999)
        outgoing_sms = []
        for sub in subs:
            sms = OutgoingSms(
                dest_msisdn=sub.dest_msisdn,
                offer_code=sub.offer_code,
                offer_name=sub.offer_name,
                text_message=message,
                smstrackcode=track_code,
            )
            outgoing_sms.append(sms)
            if len(outgoing_sms) >= 15000:
                OutgoingSms.objects.bulk_create(outgoing_sms)
                outgoing_sms.clear()
            else:
                continue
        OutgoingSms.objects.bulk_create(outgoing_sms)
        outgoing_sms.clear()
        return 'shortcode sms completed'
    elif model == 'Employee':
        subs = Employee.objects.all()
        track_code = random.randint(300, 99999)
        outgoing_sms = []
        for sub in subs:
            sms = OutgoingSms(
                dest_msisdn=sub.dest_msisdn,
                offer_code=sub.offer_code,
                offer_name=sub.offer_name,
                text_message=message,
                smstrackcode=track_code,
            )
            outgoing_sms.append(sms)
            if len(outgoing_sms) >= 15000:
                OutgoingSms.objects.bulk_create(outgoing_sms)
                outgoing_sms.clear()
            else:
                continue
        OutgoingSms.objects.bulk_create(outgoing_sms)
        outgoing_sms.clear()
        return 'shortcode sms completed'


@login_required()
def reports(request):
    text_messages = OutgoingSmsDone.objects.all()
    return render(request, 'shortcode/sms/reports.html', {'text_messages': text_messages})


@login_required()
def employer_list(request):
    if request.user.id == 187:
        employers = Employer.objects.all()
        return render(request, 'shortcode/employers/list.html', {'employers': employers})


@login_required()
def employee_list(request):
    if request.user.id == 187:
        employees = Employee.objects.all()
        return render(request, 'shortcode/employees/list.html', {'employees': employees})
