from django import forms
from .models import Stock,my_stocks

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