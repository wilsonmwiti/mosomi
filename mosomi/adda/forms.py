from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm

from adda.models import *


class RegisrationForm(UserCreationForm):
    class Meta:
        model = AddaUser
        fields = ["username", "phone_number", "county", "ward"]


class ChallengeForm(ModelForm):
    class Meta:
        model = Challenge
        fields = ['adda_user', 'title', 'county', 'description', 'date_start', 'date_end', 'phone_number']


class IdeaForm(ModelForm):
    class Meta:
        model = Idea
        fields = ['challenge', 'title', 'description', 'phone_number', 'date']


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['idea', 'phone_number', 'date', 'vote']