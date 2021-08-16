from django.contrib.auth import get_user_model
from django.db import models


class AddaUser(get_user_model()):
    phone_number = models.CharField(max_length=12)
    verification_code = models.IntegerField(null=True)
    county = models.CharField(max_length=500)
    ward = models.CharField(max_length=500)


class Challenge(models.Model):
    adda_user = models.ForeignKey(AddaUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    county = models.CharField(max_length=250)
    description = models.TextField()
    date_start = models.DateTimeField(null=True)
    status = models.BooleanField(default=False)
    date_end = models.DateTimeField(null=True)
    phone_number = models.CharField(max_length=12)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Idea(models.Model):
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    description = models.TextField()
    phone_number = models.CharField(max_length=250)
    date = models.DateTimeField()
    status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Comment(models.Model):
    idea = models.ForeignKey(Idea, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=12)
    date = models.DateTimeField()
    vote = models.CharField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class County(models.Model):
    name = models.CharField(max_length=250)