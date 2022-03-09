from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('add_stock.html', views.add_stock, name='add_stock'),
    path('delete/<stock_id>', views.delete_stock, name='delete_stock'),

]