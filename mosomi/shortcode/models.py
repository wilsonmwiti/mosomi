from django.db import models
from django.utils import timezone

from sms.models import Customer


# class Subs40892(models.Model):
#     timestamp = models.IntegerField()
#     user_id = models.IntegerField()
#     phone_number = models.CharField(max_length=16)
#     sender_name = models.CharField(max_length=300)
#     sub_date = models.DateTimeField(default=timezone.now())
#     offer_name = models.CharField(max_length=200)
#     offer_code = models.CharField(max_length=100)


class IncomingSmsSub(models.Model):
    timestamp = models.IntegerField(max_length=100)
    user_id = models.IntegerField()
    dest_msisdn = models.CharField(max_length=16)
    text_message = models.CharField(max_length=300)
    sender_name = models.CharField(max_length=300)
    link_id = models.CharField(max_length=300)
    correlator = models.CharField(max_length=300)
    send_time = models.CharField(max_length=300)
    service_id = models.CharField(max_length=300)
    product_id = models.CharField(max_length=300)
    client = models.CharField(max_length=300)
    service_type = models.IntegerField()
    sent_flag = models.CharField(max_length=300)
    export_response = models.CharField(max_length=300)
    ring_filter = models.CharField(max_length=300)
    responded = models.CharField(max_length=300)
    sub_type = models.CharField(max_length=300)
    in_date = models.DateTimeField(default=timezone.now())
    to_sub = models.IntegerField()
    processed = models.IntegerField()
    sub_status = models.CharField(max_length=200)
    offer_name = models.CharField(max_length=200)
    offer_code = models.CharField(max_length=100)


class OutgoingSms(models.Model):
    timestamp = models.IntegerField(max_length=100, default=0)
    user_id = models.IntegerField(null=True)
    dest_msisdn = models.CharField(max_length=16)
    text_message = models.CharField(max_length=300)
    delivery_status = models.CharField(max_length=300, null=True)
    link_id = models.CharField(max_length=300, null=True)
    correlator = models.CharField(max_length=300, default=0)
    send_time = models.CharField(max_length=300, null=True)
    offer_code = models.CharField(max_length=100)
    offer_name = models.CharField(max_length=100)
    product_id = models.CharField(max_length=300, null=True)
    client = models.CharField(max_length=300, null=True)
    misc = models.CharField(max_length=300, null=True)
    schedule_date = models.DateTimeField(default=timezone.now())
    oc = models.IntegerField(default=0)
    code = models.CharField(max_length=11, null=True)
    request_identifier = models.CharField(max_length=200, null=True)
    smstrackcode = models.IntegerField()
    send_date = models.DateField(null=True)
    sent = models.CharField(max_length=10, null=True)
    extra_status = models.BooleanField(default=0)


class OutgoingSmsDone(models.Model):
    timestamp = models.IntegerField(max_length=100, default=0)
    user_id = models.IntegerField(null=True)
    dest_msisdn = models.CharField(max_length=16)
    text_message = models.CharField(max_length=300)
    delivery_status = models.CharField(max_length=300, null=True)
    link_id = models.CharField(max_length=300, null=True)
    correlator = models.CharField(max_length=300, default=0)
    send_time = models.CharField(max_length=300, null=True)
    offer_code = models.CharField(max_length=100)
    offer_name = models.CharField(max_length=100)
    product_id = models.CharField(max_length=300, null=True)
    client = models.CharField(max_length=300, null=True)
    misc = models.CharField(max_length=300, null=True)
    schedule_date = models.DateTimeField(default=timezone.now())
    oc = models.IntegerField(default=0)
    code = models.CharField(max_length=11, null=True)
    request_identifier = models.CharField(max_length=200, null=True)
    smstrackcode = models.IntegerField()
    send_date = models.DateField(null=True)
    sent = models.CharField(max_length=10, null=True)
    extra_status = models.BooleanField(default=0)


class ShortCodeCustomer(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)


class Employer(models.Model):
    dest_msisdn = models.CharField(max_length=250)
    offer_name = models.CharField(max_length=250)
    text_message = models.CharField(max_length=250)
    job_category = models.CharField(max_length=250)
    job_location = models.CharField(max_length=250, null=True)
    offer_code = models.CharField(max_length=250)
    extra_satus = models.BooleanField(default=False)
    registration_date = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = 'Employer'
        verbose_name_plural = 'Employers'


class Employee(models.Model):
    dest_msisdn = models.CharField(max_length=250)
    offer_name = models.CharField(max_length=250)
    text_message = models.CharField(max_length=250)
    job_category = models.CharField(max_length=250)
    job_location = models.CharField(max_length=250, null=True)
    offer_code = models.CharField(max_length=250)
    extra_satus = models.BooleanField(default=False)
    registration_date = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = 'Employee'
        verbose_name_plural = 'Employees'