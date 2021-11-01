from django import forms
from django.db.models import fields
from .models import User
from django.contrib.auth.forms import UserCreationForm, UsernameField


class CustomUserCreationForm(UserCreationForm, UsernameField):
    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'username',
            'email',
            'phone',
        )
        field_classes = {'username': UsernameField}