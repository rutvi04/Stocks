import pandas as pd
from django.shortcuts import render,redirect
from django.http import HttpResponse, HttpRequest

from .forms import StockForm, BuyForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import login, authenticate
from .forms import SignupForm, ProfileForm
from django.urls import reverse_lazy
from django.views import generic
from .models import Profile,Stock, my_stocks, User
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
            return render(request, 'search.html', {'api': api, 'ticker': ticker})

        except Exception as e:
            api = "Error..."
            messages.error(request,("Please enter valid symbol"))
            return redirect('index')

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
            ticker = request.POST['ticker']
            api_request = requests.get(
                "https://cloud.iexapis.com/stable/stock/" + ticker + "/quote?token=pk_0dff57f16e54425eb2601c2a89a23edf")
            try:
                api = json.loads(api_request.content)
                instance = form.save(commit=False)
                instance.author = request.user
                instance.save()
                messages.success(request, ("Stock has been added!"))

            except Exception as e:
                api = "Error..."
                messages.error(request,("Enter Valid Symbol"))
            return redirect('watchlist')

    else:
        ticker = Stock.objects.filter(author = request.user)
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
    ticker = Stock.objects.filter(author = request.user)
    return render(request, 'delete.html', {'ticker':ticker})

def news(request):
    request_api = requests.get('https://stocknewsapi.com/api/v1/category?section=general&items=50&token=zoiv7dexarnbjd4anbtduzucjw5bdjk5xxqpd93d')
    news_api = json.loads(request_api.content)
    return render(request, 'news.html', {'news_api' : news_api})

def buy_stock(request):
    if request.method == 'POST':
        symbol = request.POST['symbol']
        latest_price = float(request.POST['latest_price'])
       # quantity = float(my_stocks.objects.get(my_author=request.user).quantity)

        availableBal= Profile.objects.get(user=request.user).available_bal
        # available_bal = available_bal- (latest_price*quantity)

        api_request = requests.get(
            "https://cloud.iexapis.com/stable/stock/" + symbol + "/quote?token=pk_0dff57f16e54425eb2601c2a89a23edf")
        try:
            api = json.loads(api_request.content)
        except Exception as e:
            api = "Error..."
        return render(request, 'buy_stock.html', {'api': api, 'symbol': symbol,'availableBal':availableBal})
    else:
        messages.error(request,("Errorr"))
        return render(request,'watchlist.html', {})


def myportfolio(request):
    symbol = request.POST['stock_symbol']
    list_stock= []
    #availableBal = Profile.objects.get(user=request.user).available_bal
    api_request = requests.get(
        "https://cloud.iexapis.com/stable/stock/" + symbol + "/quote?token=pk_0dff57f16e54425eb2601c2a89a23edf")
    try:
        api = json.loads(api_request.content)
    except Exception as e:
        api = "Error..."
    if request.method == 'POST':
        form = BuyForm(request.POST)

        if form.is_valid():
            quantity = request.POST['quantity']
            latest_price = request.POST['latest_price']
            #quantity = my_stocks.objects.get(my_author=request.user).quantity
            availableBal = Profile.objects.get(user=request.user).available_bal
            #availableBal = 20000
            buyAmount = float(quantity)*float(latest_price)
            if availableBal >= buyAmount:
                availableBal -= buyAmount
                P = Profile.objects.get(user=request.user)
                P.available_bal = availableBal
                P.save()
                #ms = my_stocks.objects.get(my_author=request.user)

               # Profile.objects.filter(user=(Profile.objects.get(user=request.user))).update(available_bal = 'availableBal')
               # Profile.objects.get(user=request.user).update(available_bal = 'availableBal')

               # availableBal.save(update_fields=['available_bal'])

                instance = form.save(commit=False)
                instance.stock_symbol = symbol
                instance.my_author = request.user
                instance.price = latest_price
                instance.save()
                messages.success(request, ("You have bought the stock!"))
                context = {'buyAmount': buyAmount , 'availableBal': availableBal, 'symbol': symbol, 'api': api,'quantity': quantity,'list_stock': list_stock}
                return render(request, 'myportfolio.html', context)
            else:

                newform = BuyForm()

                messages.success(request,("You don't have sufficient balance!"))
                return render(request,'buy_stock.html',{'BuyForm' : newform,'symbol': symbol, 'api': api,'availableBal': availableBal})

        else:
            newform = BuyForm()
            availableBal = Profile.objects.get(user=request.user).available_bal
            note = form.errors
            messages.error(request,("Please enter valid values"))
            return render(request, 'buy_stock.html', {'BuyForm' : newform, 'note': note,'symbol': symbol, 'api': api, 'availableBal': availableBal})
    else:
        form = BuyForm()
        availableBal = Profile.objects.get(user=request.user).available_bal
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

def add_fund(request):
    if request.method == 'POST':
        availableBal = Profile.objects.get(user=request.user).available_bal


        availableBal += float(request.POST['amount'])
        Profile.objects.filter(user=request.user).update(available_bal=availableBal)

        messages.success(request, ("Fund has been added!"))
        return render(request,'add_fund.html', {'availableBal': availableBal})
    else:
        availableBal = Profile.objects.get(user=request.user).available_bal
        # messages.error(request,("Something went wrong. Sorry!!"))

        return render(request,'add_fund.html',{'availableBal':availableBal})
   #if request.method == 'POST':
        #P = Profile.objects.get(user=request.user)

        #available_bal = P.available_bal

        #return render(request,'add_fund.html', {'available_bal': available_bal, 'static': 40000})
        # return redirect('index')
    #else:
        #return redirect('watchlist')"""



#def quantity(request):
  #  if request.method == 'POST':
  #      quantity = request.POST['quantity']
  #      latest_price = request.POST['latest_price']
  #      total_funds = quantity * latest_price
  #      return redirect(buy_stock('total_funds'))

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        profile_form = ProfileForm(request.POST, request.FILES)
        if form.is_valid() and profile_form.is_valid():
            user = form.save()
            profile= profile_form.save(commit=False)
            profile.user = user
            img_obj = profile_form.instance
            profile.save()
            username = form.cleaned_data.get('username')
            pwd = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=pwd)
            login(request, user)
            return redirect('index')
        else:
            form = SignupForm()
            profile_form = ProfileForm
            messages.error(request,("Please enter valid details"))
            return render(request, 'registration/signup.html', {'form': form, 'profile_form': profile_form})
    else:
        form = SignupForm()
        profile_form = ProfileForm()
        return render(request, 'registration/signup.html', {'form': form, 'profile_form': profile_form})


# @transaction.atomic
@login_required
def profile(request):
    if request.method == 'POST':
        user_form = SignupForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile was successfully updated!')
            return redirect('edit_profile')
    # else:
            # messages.error(request, _('Please correct the error below.'))
    else:
        user_form = SignupForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
        context = {'user_form': user_form,'profile_form': profile_form,'available_bal': Profile.objects.get(user=request.user).available_bal, 'invested_bal': Profile.objects.get(user=request.user).invested_bal}
    return render(request, 'registration/edit_profile.html', context)

def portfolio(request):

    holding_list = my_stocks.objects.filter(my_author=request.user)
    #buy_list = []
    #for holding in holding_list:
    return render(request,'portfolio.html',{'holding_list': holding_list})
