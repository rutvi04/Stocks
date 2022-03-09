from django.shortcuts import render,redirect
from django.http import HttpResponse, HttpRequest
from .models import Stock
from .forms import StockForm
from django.contrib import messages
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

    if request.method == 'POST':
        form = StockForm(request.POST or None)

        if form.is_valid():
            form.save()
            messages.success(request,("Stock has been added!"))
            return redirect('add_stock')
    else:
        ticker = Stock.objects.all()
        return render(request, 'add_stock.html', {'ticker' : ticker})


def delete_stock(request, stock_id):
    item = Stock.objects.get(pk=stock_id)
    item.delete()
    messages.success(request, ("Stock has been deleted!"))
    return redirect(add_stock)