from django.urls import path

from sms_api import views

urlpatterns = [
    path('roberms/get/access/token', views.get_access_token, name='get_access_token'),
    path('roberms/send/simple/sms', views.simple_sms, name='simple_sms'),
    path('roberms/willinya/send/simple/sms', views.willinya_simple_sms, name='willinya_simple_sm'),
    path('roberms/send/bulk/sms', views.bulk_sms, name='bulk_sms'),
    path('roberms/register/urls', views.register_urls, name='register_urls'),
    path('roberms/trial', views.generate_sample_request, name='g'),
    path('roberms/willinya', views.receive_message_count, name='receive_message_count'),
    path('credit/balance', views.get_credit_balance, name='get_credit_balance'),

    path('credit/balance/test', views.generate_credit_sample_request),
]