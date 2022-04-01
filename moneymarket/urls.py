from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('search', views.search, name='search'),
    path('watchlist', views.watchlist, name='watchlist'),
    path('delete.html', views.delete, name='delete'),
    path('delete/<stock_id>', views.delete_stock, name='delete_stock'),
    path('about/', views.about, name='about'),
    path('buy_stock.html', views.buy_stock, name='buy_stock'),
    path('myportfolio.html', views.myportfolio, name= 'myportfolio')


]