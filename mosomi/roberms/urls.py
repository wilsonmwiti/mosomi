from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.contrib.auth import views as auth_views, views

from roberms import settings

urlpatterns = [
    path('password_change/', views.PasswordChangeView.as_view(), name='password_change'),
    path('password_change/done/', views.PasswordChangeDoneView.as_view(), name='password_change_done'),

    path('password_reset/', views.PasswordResetView.as_view(
        template_name='r/password_reset_form.html'), name='password_reset'),
    path('password_reset/done/', views.PasswordResetDoneView.as_view(template_name='r/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', views.PasswordResetConfirmView.as_view(template_name='r/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', views.PasswordResetCompleteView.as_view(template_name='r/password_reset_complete.html'), name='password_reset_complete'),
    # url('^', include('django.contrib.auth.urls')),


    url(r'^admin/', include('admin_honeypot.urls', namespace='admin_honeypot')),
    path('roberms/super/admin/', admin.site.urls),

    path('', include('sms.urls')),
    path('sms/v1/', include('sms_api.urls')),
    path('roberms/admin/', include('roberms_admin.urls')),
    path('roberms/salesperson/', include('salesperson.urls')),
    path('invoices/', include('invoices.urls')),
    path('api/v1/', include('mpesa_api.urls')),
    path('school/', include('school.urls')),
    path('shortcode/', include('shortcode.urls')),
    path('adda/', include('adda.urls')),
    path('login/', auth_views.LoginView.as_view(), name='login'),

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
