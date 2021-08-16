from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import formset_factory

from school.models import *


class SchoolAdminForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.Meta.required:
            self.fields[field].required = False

    class Meta:
        model = SchoolAdmin
        fields = ("username", "email", "password1", "password2", "phone_number", "school",)
        required = ("school",)


class SchoolForm(forms.ModelForm):
    class Meta:
        model = School
        fields = ("name", "address", "location", "school_type",)


class FeeForm(forms.ModelForm):
    class Meta:
        model = FeeBreakDown
        fields = ("name", "percentage", "term_year")