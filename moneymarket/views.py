import pandas as pd
from django.shortcuts import render,redirect
from django.http import HttpResponse, HttpRequest
from .models import Stock, my_stocks
from .forms import StockForm, BuyForm
from django.contrib import messages

from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import login, authenticate
from .forms import SignupForm, ProfileForm
from django.urls import reverse_lazy
from django.views import generic
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
            instance = form.save(commit=False)
            instance.author = request.user
            instance.save()
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
    list_items = Stock.objects.get(pk=stock_id)
    list_items.delete()
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
    symbol = request.POST['symbol']
    api_request = requests.get(
        "https://cloud.iexapis.com/stable/stock/" + symbol + "/quote?token=pk_0dff57f16e54425eb2601c2a89a23edf")
    try:
        api = json.loads(api_request.content)
    except Exception as e:
        api = "Error..."
    availableBal = 30000
    if request.method == 'POST':
        form = BuyForm(request.POST)

        if form.is_valid():
            quantity = request.POST['quantity']
            latest_price = request.POST['latest_price']

            buyAmount = float(quantity)*float(latest_price)
            if availableBal >= buyAmount:
                availableBal -= buyAmount
                instance = form.save(commit=False)
                instance.my_author = request.user
                instance.save()
                messages.success(request, ("You have bought the stock!"))
                return render(request, 'myportfolio.html', {'buyAmount': buyAmount , 'availableBal': availableBal, 'symbol': symbol, 'api': api})
            else:

                newform = BuyForm()

                messages.success(request,("You don't have sufficient balance!"))
                return render(request,'buy_stock.html',{'BuyForm' : newform,'symbol': symbol, 'api': api,'availableBal': availableBal})

        else:
            newform = BuyForm()
            note = form.errors
            messages.error(request,("Please enter valid values"))
            return render(request, 'buy_stock.html', {'BuyForm' : newform, 'note': note,'symbol': symbol, 'api': api, 'availableBal': availableBal})

    elif request.method == 'POST':
        form = BuyForm(request.POST)
        buyAmount = 30000
        if form.is_valid():
            quantity = request.POST['quantity']
            latest_price = request.POST['latest_price']

            sellAmount = float(quantity)*float(latest_price)
            if buyAmount >= sellAmount:
                availableBal += sellAmount
                instance = form.save(commit=False)
                instance.my_author = request.user
                instance.save()
                messages.success(request, ("You have sold the stock!"))
                return render(request, 'myportfolio.html', {'buyAmount': buyAmount , 'availableBal': availableBal, 'symbol': symbol, 'api': api})
            else:

                newform = BuyForm()

                messages.success(request,("You don't have sufficient balance!"))
                return render(request,'sell_stock.html',{'BuyForm' : newform,'symbol': symbol, 'api': api,'buyAmount': buyAmount})

        else:
            newform = BuyForm()
            note = form.errors
            messages.error(request,("Please enter valid values"))
            return render(request, 'sell_stock.html', {'BuyForm' : newform, 'note': note,'symbol': symbol, 'api': api, 'buyAmount': buyAmount})

    else:
        form = BuyForm()
        return render(request,'buy_stock.html', {'BuyForm': form, 'symbol': symbol, 'api': api, 'availableBal': availableBal})



 ##           form.save()
 ##           messages.success(request,("Stock has been added to the holding"))
 ##           return redirect('watchlist')
 ##   else:
 ##       ticker = BuyForm.objects.all()
 ##       output = []
 ##       for ticker_items in ticker:
 ##           api_request = requests.get(
 ##               "https://cloud.iexapis.com/stable/stock/" + str(ticker_items) + "/quote?token=pk_0dff57f16e54425eb2601c2a89a23edf")
 ##           try:
 ##               api = json.loads(api_request.content)
 ##               output.append(api)
 ##           except Exception as e:
 ##               api = "Error..."
 ##       return render(request, 'watchlist.html', {'ticker' : ticker, 'output': output})
##
 ##   return render(request, 'myportfolio.html', {})

##def buy_stock(request):
 ##       form = BuyForm(request.POST or None)
 ##       total_funds = quantity()
 ##       availableBalance = 2000
 ##       if form.is_valid():
  #          form.save()
  #          if availableBalance > total_funds:
  #              messages.success(request,("Stock has been added to your Holding"))
  #              return render(request, 'myportfolio.html', {'total_funds': total_funds, 'availableBalance': availableBalance})
  #             return render(request, 'buy_stock.html', {})
   #     else:
  #          form = BuyForm()
  #          return render(request, 'buy_stock.html', {})

def buy_stock(request):
    if request.method == 'POST':
        symbol = request.POST['symbol']
        api_request = requests.get(
            "https://cloud.iexapis.com/stable/stock/" + symbol + "/quote?token=pk_0dff57f16e54425eb2601c2a89a23edf")
        try:
            api = json.loads(api_request.content)
        except Exception as e:
            api = "Error..."
        return render(request, 'buy_stock.html', {'api': api, 'symbol': symbol, 'availableBal': 30000})

def sell_stock(request):
    if request.method == 'POST':
        symbol = request.POST['symbol']
        api_request = requests.get(
            "https://cloud.iexapis.com/stable/stock/" + symbol + "/quote?token=pk_0dff57f16e54425eb2601c2a89a23edf")
        try:
            api = json.loads(api_request.content)
        except Exception as e:
            api = "Error..."
        return render(request, 'sell_stock.html', {'api': api, 'symbol': symbol, 'buyAmount': 30000})


#def quantity(request):
  #  if request.method == 'POST':
  #      quantity = request.POST['quantity']
  #      latest_price = request.POST['latest_price']
  #      total_funds = quantity * latest_price
  #      return redirect(buy_stock('total_funds'))

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        profile_form = ProfileForm(request.POST)
        if form.is_valid() and profile_form.is_valid():
            user = form.save()
            profile= profile_form.save(commit=False)
            profile.user = user

            profile.save()

            username = form.cleaned_data.get('username')
            pwd = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=pwd)
            login(request, user)
            return redirect('index')
        else:
            note = form.errors
            return render(request, 'registration/signup.html', {'note': note})
    else:
        form = SignupForm
        profile_form = ProfileForm()
        note = form.errors
        return render(request, 'registration/signup.html', {'form': form, 'note':note, 'profile_form': profile_form})



# @login_required
# @transaction.atomic
#def profile(request):
 #   if request.method == 'POST':
  #      user_form = SignupForm(request.POST, instance=request.user)
  #      profile_form = ProfileForm(request.POST, instance=request.user.profile)
  #      if user_form.is_valid() and profile_form.is_valid():
  #          user_form.save()
  #          profile_form.save()
  #          messages.success(request, _('Your profile was successfully updated!'))
  #          return redirect('settings:profile')
 #       else:
 #           messages.error(request, _('Please correct the error below.'))
 #   else:
 #       user_form = SignupForm(instance=request.user)
#    return render(request, 'profile.html', {
      #  'user_form': user_form,
       # 'profile_form': profile_form
#    })
#

class UserEditView(generic.UpdateView):
    form_class = UserChangeForm
    profile_form = ProfileForm
    template_name = "registration/edit_profile.html"
    success_url = reverse_lazy('index')


    def get_object(self):
        return self.request.user


