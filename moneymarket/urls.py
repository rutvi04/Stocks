from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('search/<str:symb>', views.search, name='search'),
    path('watchlist.html', views.watchlist, name='watchlist'),
    path('delete.html', views.delete, name='delete'),
    path('delete/<stock_id>', views.delete_stock, name='delete_stock'),
    path('about.html', views.about, name='about'),


]