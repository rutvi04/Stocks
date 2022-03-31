import pandas as pd
from django.shortcuts import render,redirect
from django.http import HttpResponse, HttpRequest
from .models import Stock
from .forms import StockForm
from django.contrib import messages
import requests
import json
# Create your views here.

def index(request):
    ticker = ['aapl','msft','2222.sr','goog','amzn','tsla','brk-a','nvda','fb','tsm','unh','v','jnj','tcehy','wmt','005930.ks','pg','lvmuy','nsrgy','ma','xom','rhhby','bac','baba']
    output = []
    for ticker_items in ticker:
            api_request = requests.get(
                "https://cloud.iexapis.com/stable/stock/" + str(ticker_items) + "/quote?token=pk_0dff57f16e54425eb2601c2a89a23edf")
            try:
                api = json.loads(api_request.content)
                output.append(api)
            except Exception as e:
                api = "Error..."
    return render(request, 'index.html', {'ticker': ticker, 'output': output})

def search(request,symb):
    if request.method == 'POST':
        ticker = request.POST['ticker']
        api_request = requests.get(
            "https://cloud.iexapis.com/stable/stock/" + ticker + "/quote?token=pk_0dff57f16e54425eb2601c2a89a23edf")
        try:
            api = json.loads(api_request.content)
        except Exception as e:
            api = "Error..."
        return render(request, 'search.html', {'api': api, 'ticker': ticker})
        # pk_5d448bc5ec78430f9f18a309b283a812ch
    elif symb:
        ticker = symb
        api_request = requests.get(
            "https://cloud.iexapis.com/stable/stock/" + ticker + "/quote?token=pk_0dff57f16e54425eb2601c2a89a23edf")
        try:
            api = json.loads(api_request.content)
        except Exception as e:
            api = "Error..."
        return render(request, 'search.html', {'api': api, 'ticker': ticker})
    else:
        return render(request,'search.html', {'ticker': "Enter the symbol above"})




def watchlist(request):
    import requests
    import json

    if request.method == 'POST':
        form = StockForm(request.POST or None)

        if form.is_valid():
            form.save()
            messages.success(request,("Stock has been added!"))
            return redirect('watchlist')
    else:
        ticker = Stock.objects.all()
        output = []
        for ticker_items in ticker:
            api_request = requests.get(
                "https://cloud.iexapis.com/stable/stock/" + str(ticker_items) + "/quote?token=pk_0dff57f16e54425eb2601c2a89a23edf")
            try:
                api = json.loads(api_request.content)
                output.append(api)
            except Exception as e:
                api = "Error..."
        return render(request, 'watchlist.html', {'ticker' : ticker, 'output': output})


def delete_stock(request, stock_id):
    item = Stock.objects.get(pk=stock_id)
    item.delete()
    messages.success(request, ("Stock has been deleted!"))
    return redirect(delete)

def delete(request):
    ticker = Stock.objects.all()
    return render(request, 'delete.html', {'ticker':ticker})

def about(request):
    request_api = requests.get('https://stocknewsapi.com/api/v1/category?section=general&items=50&token=zoiv7dexarnbjd4anbtduzucjw5bdjk5xxqpd93d')
    news_api = json.loads(request_api.content)
    return render(request, 'about.html', {'news_api' : news_api})