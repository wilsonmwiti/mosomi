from django.urls import path

from shortcode import views

app_name = 'ShortCode'
urlpatterns = [
    # path('subs', views.subs, name='subs'),
    path('incoming/sms', views.incoming_sms, name='incoming_sms'),
    path('send', views.simple_sms, name='simple_sms'),
    path('reports', views.reports, name='reports'),
    path('employers', views.employer_list, name='employers'),
    path('employees', views.employee_list, name='employees'),
]