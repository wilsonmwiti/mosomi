from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from django.urls import path

from sms import views
from django.contrib.auth import views as auth_views

from sms.views import OrderListJson, OrderReportJson, AllMessagesJson

app_name = 'sms'
urlpatterns = [
    # path('login', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('login', views.roberms_login, name='login'),
    path('logout', auth_views.LogoutView.as_view(template_name='registration/logout.html'), name='logout'),
    path('verify/account', views.verify_account, name='verify_account'),
    path('', views.home, name='sms-home'),
    path('profile', views.profile, name='profile'),
    path('about', views.about, name='about'),
    path('services', views.services, name='services'),
    path('contact', views.contact, name='contact'),

    # customer
    path('apps', views.apps, name='apps'),
    path('send/', views.send, name='send'),
    path('simple/sms', views.simple_sms, name='simple_sms'),
    path('simple/sms/preview', views.simple_sms_preview, name='simple_sms_preview'),
    path('import/csv', views.import_csv_2, name='import_csv'),
    path('merge', views.merge_sms_2, name='merge_sms'),
    path('confirm', views.confirm, name='confirm'),
    path('customer/reports/<int:tracking_code>', views.reports, name='customer_reports'),
    path('customer/credit', views.customer_credit, name='customer_credit'),
    path('customer/contacts', views.customer_contacts, name='customer_contacts'),
    path('customer/comprehensive/reports', views.comprehensive_reports, name='comprehensive_reports'),
    path('sent/report/details/<str:track_code>', views.report_details, name='report_details'),
    path('generate/sms/report/<str:track_code>', views.generate_sms_report, name='generate_sms_report'),
    path('personalized/sms/menu', views.personalized_sms_menu, name='personalized_sms_menu'),
    path('personalized/contacts', views.personalized_from_contact_list, name='personalized_contacts'),
    # path('choose/contact/personalized/contactsgroups', views.choose_contact_groups, name='choose_contact_groups'),
    path('contact/list/sample/merged', views.c_sample_merged, name='c_sample_merged'),
    path('messages/dashboard', views.messages_dashboard, name='messages_dashboard'),

    # groups
    path('create/group', views.create_group, name='create_group'),
    path('group/contacts/<int:group_id>', views.group_contacts, name='group_contacts'),
    path('create/group/contact/<int:group_id>', views.create_contact, name='create_group_contact'),
    path('import/group/contacts/<int:group_id>', views.import_contacts, name='import_contacts'),
    path('delete/group/<int:group_id>', views.delete_group, name='delete_group'),
    path('monthly/credit/usage', views.credit_used, name='credit_usage'),
    path('delete/contacts/<int:contact_id>', views.delete_contact, name='delete_contact'),
    path('update/group/<int:group_id>', views.update_group, name='update_group'),
    path('update/contact/<int:contact_id>', views.update_contact, name='update_contact'),
    # path('delete/contact/<int:g')

    path('simple', views.SendSmsView.as_view(), name='sms-simple'),
    path('smsreport', views.SmsReportView.as_view(), name='sms-simple'),
    path('sms/reports', views.sms_reports, name='my_sms_reports'),
    # path('send/sms', views.send_sms, name='send_sms'),
    # path('get/sms/delivery/status', views.get_delivery_status, name='get_delivery_status'),

    #top up
    path('payment/verification', views.verify_payment, name='verify_payment'),
    path('register', views.register, name='register'),
    path('edit/profile', views.edit_profile, name='edit_profile'),

    # till_numbers
    path('till/numbers', views.customer_till_numbers, name='customer_till_numbers'),
    path('add/till/number', views.add_till_number, name='add_till_number'),
    path('edit/till/number/<int:till_number_id>', views.edit_till_number, name='edit_till_number'),
    path('delete/till/number/<int:till_number_id>', views.delete_till_number, name='delete_till_number'),

    #contacts
    path('activate/deactivate/contact/<int:contact_id>', views.activate_deactivate_contact, name='activate_deactivate_contact'),

    #celery
    path('contacts/upload/status/<str:task_id>', views.contacts_upload_status, name='contacts_upload_status' ),
    path('poll_contact_upload_state/<str:task_id>', views.poll_contact_upload_state, name='poll_contact_upload_state'),

    #trial
    path('get/token', views.trial, name='trial'),

    #docs
    path('documentation', views.documentation, name='documentation'),

    #sender name
    path('sender_name/applications', views.applications, name='applications'),
    path('new/sender_name/application', views.new_application, name='new_application'),
    path('application/contacts/<int:application_id>', views.application_contacts, name='application_contacts'),
    path('add/application/contact/<int:application_id>', views.add_application_contacts, name='add_application_contact'),
    path('download/application/<int:application_id>', views.show_pdf, name='show_pdf'),

    #inbox
    # path('inbox', views.inbox, name='inbox'),

    path('offers', views.offers, name='offers'),
    path('new/tag', views.new_tag, name='new_tag'),
    path('tags', views.get_tags, name='get_tags'),
    path('tag/messages/<int:tag_id>', views.tag_messages, name='tag_messages'),

    path('express/import/contacts/<int:group_id>', views.express_import_contacts, name='express_import_contacts'),

    path('clean/contacts', views.temp_clean_sys),

    #datatables
    path('my/datatable/data/<int:group_id>/', login_required(OrderListJson.as_view()), name='order_list_json'),
    path('sample/datatable/<int:group_id>', views.sample_datatable, name='sample_datatable'),

    path('draw/<str:track_code>', login_required(OrderReportJson.as_view()), name='order_report_json'),
    path('json/all/messages', login_required(AllMessagesJson.as_view()), name='all_messages_json'),

    path('my/payments', views.my_payments, name="my_payments"),
    path('add/patient', views.st_ann_add_patient, name='st_ann_add_patient'),
]