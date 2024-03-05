from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from .models import CustomUser, Tenant, Broker


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ("email", "password")


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ("email",)


class TenantsForm(forms.ModelForm):
    email = forms.EmailField()
    password = forms.CharField()

    class Meta:
        model = Tenant
        fields = ["email", "password", "name"]
        exclude = ['user', 'broker', 'property_manager']


class BrokerForm(forms.ModelForm):
    email = forms.EmailField()
    password = forms.CharField()

    class Meta:
        model = Broker
        fields = ["email", "password", "name"]
        exclude = ['user', 'broker', 'property_manager']
