from django.urls import path

from invoices import views

app_name = 'Invoices'
urlpatterns = [
    path('create_invoice/<int:client_id>', views.create_invoice, name='create_invoice'),
    path('client_invoices/<int:client_id>', views.client_invoices, name='client_invoices'),
    path('create_client', views.create_client, name='create_client'),
    path('invoice_clients', views.invoice_clients, name='invoice_clients'),
    path('invoice/services/<int:invoice_id>', views.invoice_services, name='invoice_services'),
    path('add_invoice_services/<int:invoice_id>', views.add_invoice_services, name='add_invoice_services'),
    path('invoice/preview/<int:invoice_id>', views.invoice_preview, name='invoice_preview'),
    path('invoice/payments/<int:invoice_id>', views.invoice_payments, name='invoice_payments'),
    path('add/invoice/payment/<int:invoice_id>', views.add_payment, name='add_payment'),
    path('mark/invoice/as/payed/<int:invoice_id>', views.mark_invoice_as_payed, name='mark_invoice_as_payed'),
    path('delete/invoice/service/<int:service_id>', views.delete_service, name='delete_service'),
    path('delete/invoice/<int:invoice_id>', views.delete_invoice, name='delete_invoice'),

    path('edit/invoice/<int:invoice_id>', views.edit_invoice, name='edit_invoice'),
    path('edit/invoice/service/<int:service_id>', views.edit_invoice_service, name='edit_invoice_service'),

    path('edit/client/<int:client_id>', views.edit_client, name='edit_client'),
]