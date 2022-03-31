from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('search/<str:symb>', views.search, name='search'),
    path('add_stock.html', views.add_stock, name='add_stock'),
    path('delete.html', views.delete, name='delete'),
    path('delete/<stock_id>', views.delete_stock, name='delete_stock'),
    path('about.html', views.about, name='about'),


]