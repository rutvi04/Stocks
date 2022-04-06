from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name='index'),
    path('search', views.search, name='search'),
    path('watchlist', views.watchlist, name='watchlist'),
    path('delete.html', views.delete, name='delete'),
    path('delete_stock/<stock_id>', views.delete_stock, name='delete_stock'),
    path('news/', views.news, name='news'),
    path('buy_stock/', views.buy_stock, name='buy_stock'),
    path('myportfolio.html', views.myportfolio, name= 'myportfolio'),
    path('edit_profile/', views.profile, name='edit_profile'),
    path('add_fund/', views.add_fund, name='add_fund'),
    path('accounts/signup',views.signup,name='signup'),
    path('portfolio',views.portfolio, name='portfolio'),
    path('accounts/password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('accounts/password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name = 'password_reset_done'),
    path('accounts/reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name = 'password_reset_confirm'),
    path('accounts/reset/done/', auth_views.PasswordResetCompleteView.as_view(), name = 'password_reset_complete'),



]