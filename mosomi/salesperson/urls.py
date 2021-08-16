from django.urls import path
from salesperson import views

app_name = 'salesperson'
urlpatterns = [
    path('dashboard', views.dashboard, name='dashboard'),
    path('clients', views.clients, name='clients'),
    path('client/top/ups/<int:client_id>', views.client_top_ups, name='client_top_ups'),
    path('top_ups', views.all_top_ups, name='all_top_ups'),
    path('account/usage', views.account_usage, name='account_usage'),
    # path('/add/client', views.add_client, name='add_client')
    # path('/sales_people', views.sales_people, name='sales_people'),
    # path('/add_sales_person', views.add_sales_person, name='add_sales_person')

    path('my/companies', views.my_companies, name='my_companies'),
    path('company/appointments/<int:company_id>', views.appointment_list, name='company_appointments'),
    path('add/company', views.add_company, name='add_company'),
    path('edit/company/<int:company_id>', views.edit_company, name='edit_company'),
    path('add/appointment/<int:company_id>', views.add_appointment, name='add_appointment'),
    path('edit/appointment/<int:appointment_id>', views.edit_appointment, name='edit_appointment'),

    path('mark_visited_not_visited/<int:appointment_id>', views.mark_visited_not_visited, name='mark_visited_not_visited'),
]