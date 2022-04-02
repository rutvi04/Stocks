import pandas as pd
from django.shortcuts import render,redirect
from django.http import HttpResponse, HttpRequest
from .models import Stock, my_stocks
from .forms import StockForm, BuyForm
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

def search(request):
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

    elif request.method == 'GET':
        ticker=request.GET['ticker']
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

def myportfolio(request):
    if request.method == 'POST':
        form = StockForm(request.POST or None)

        if form.is_valid():
            form.save()
            messages.success(request,("Stock has been added to the holding"))
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

    return render(request, 'myportfolio.html', {})

def buy_stock(request):
        form = BuyForm(request.POST or None)
        total_funds = quantity()
        availableBalance = 2000
        if form.is_valid():
            form.save()
            if availableBalance > total_funds:
                messages.success(request,("Stock has been added to your Holding"))
                return render(request, 'myportfolio.html', {'total_funds': total_funds, 'availableBalance': availableBalance})
            else:
                messages.success(request,("You do not have enough balance"))
                return render(request, 'buy_stock.html', {})
        else:
            form = BuyForm()
            return render(request, 'buy_stock.html', {})

def buy(request):
    if request.method == 'POST':
        company_name = request.POST['company_name']
        latest_price = request.POST['latest_price']
        return render(request, 'buy_stock.html',{'company_name': company_name, 'latest_price': latest_price})

def quantity(request):
    if request.method == 'POST':
        quantity = request.POST['quantity']
        latest_price = request.POST['latest_price']
        total_funds = quantity * latest_price
        return redirect(buy_stock('total_funds'))


