from django.urls import path

from roberms_admin import views

app_name = 'roberms_admin'
urlpatterns = [
    path('dashboard', views.dashboard, name='dashboard'),
    path('clients', views.clients, name='clients'),
    path('sales_people', views.sales_people, name='sales_people'),
    path('add_sales_person', views.add_sales_person, name='add_sales_person'),
    path('assign/client/<int:sales_person_id>', views.assign_client, name='assign_client'),
    path('sales_person_clients/<int:sales_person_id>', views.sales_person_clients, name='sales_person_clients'),
    path('delete/sales/person/<int:person_id>', views.delete_sales_person, name='delete_sales_person'),
    path('activate_deactivate_sales_person/<int:person_id>', views.activate_deactivate_sales_person, name='activate_deactivate'),

    path('top/ups', views.top_ups, name='top_ups'),
    path('add/top/up', views.add_client_credit, name='add_top_up'),

    path("client/top_ups/<int:client_id>", views.client_top_ups, name='client_top_ups'),

    path('mark_commission_paid/<int:top_up_id>', views.mark_commission_paid, name='mark_commission_paid'),
    path('account/usage', views.account_usage, name='account_usage'),

    #dummy
    path('sample/images', views.client_images, name='client_images'),

    path('change/sender_id/<int:client_id>', views.client_edit, name='customer_edit'),

    path('sales/people/list', views.list_sales_people, name='list_sales_people'),
    path('sales/person/companies/<int:sales_person_id>', views.sales_person_companies, name='sales_person_companies'),
    path('company/appointments/<int:company_id>', views.company_appointments, name='company_appointments'),
]