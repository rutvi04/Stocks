from django.urls import path
from . import views
from .views import UserEditView

urlpatterns = [
    path('', views.index, name='index'),
    path('search', views.search, name='search'),
    path('watchlist', views.watchlist, name='watchlist'),
    path('delete.html', views.delete, name='delete'),
    path('delete_stock/<stock_id>', views.delete_stock, name='delete_stock'),
    path('about/', views.about, name='about'),
    path('buy_stock.html', views.buy_stock, name='buy_stock'),
    path('sell_stock.html', views.sell_stock, name='sell_stock'),
    # path('buy/', views.buy, name='buy'),
   # path('quantity/', views.quantity, name='quantity'),
    path('myportfolio.html', views.myportfolio, name= 'myportfolio'),
    path('edit_profile/', UserEditView.as_view(), name='edit_profile'),
    path('accounts/signup',views.signup,name='signup'),



]