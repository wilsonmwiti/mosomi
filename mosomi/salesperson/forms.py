from django import forms
from roberms_admin.models import Company


class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ('name', 'phone_number', 'contact_person',
                  'email', 'sales_person', 'location')