from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from sms.models import *


# class CustomerDetailsForm(forms.ModelForm):
#     class Meta:
#         model = Customer
#         fields = ('location', 'phone_number')


# class UserRegisterForm(UserCreationForm):
#     class Meta:
#         model = User
#         fields = ["username", "email", "password1", "password2"]

class CustomerRegisrationForm(UserCreationForm):
    class Meta:
        model = Customer
        fields = ("username", "phone_number")


class SendForm(forms.Form):

    class Meta:
        model = Outgoing
        fields = ["phone_numbers", "text_message"]



