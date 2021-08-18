from django import forms
from django.forms import ModelForm
from .models import *
from django.contrib.auth.forms import UserCreationForm


class ProductCreateForm(ModelForm):

    class Meta:
        model = Products
        fields = ['name', 'descriptions', 'price', 'quantity',]

class ReturnsForm(ModelForm):

    class Meta:
        model = Return
        fields = []

class Registration(UserCreationForm):

    class Meta:
        model = Costumer
        fields = ['username', 'password1', 'password2']

class BuyForm(ModelForm):
    class Meta:
        model = Purcase
        fields = ["quantity"]       
