from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
from .models import Stock
# Create your views here.

def index(request):
    import requests
    import json
    if request.method == 'POST':
        ticker = request.POST['ticker']
        api_request = requests.get(
            "https://cloud.iexapis.com/stable/stock/" + ticker + "/quote?token=pk_0dff57f16e54425eb2601c2a89a23edf")
        try:
            api = json.loads(api_request.content)
        except Exception as e:
            api = "Error..."
        return render(request, 'index.html', {'api': api})
        # pk_5d448bc5ec78430f9f18a309b283a812
        # XTRyuTSxOF0KKDoTxdVI5hRSRjGrRB0g
    else:
        return render(request,'index.html', {'ticker': "Enter a Ticker Symbol Above..."})
#pk_0dff57f16e54425eb2601c2a89a23edf

def about(request):
    return render(request, 'about.html', {})

def add_stock(request):

    ticker = Stock.objects.all()
    return render(request, 'add_stock.html', {'ticker' : ticker})