from django import forms
from .models import Stock,my_stocks, User, Profile
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy

class StockForm (forms.ModelForm):
    class Meta:
        model=Stock
        fields = ["ticker"]

class BuyForm(forms.ModelForm):
    class Meta:
        model =my_stocks
        fields = ['quantity',]
        widget = {
          #  'stock_symbol': forms.TextInput,
            'quantity': forms.IntegerField
        }
        labels = {
           # 'stock_symbol': 'Stock Symbol',
            'quantity': 'Total Quantity'
        }


class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username', 'password1', 'password2')


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('UID', 'address', 'demat_ac', 'bank_ac', 'gender')

