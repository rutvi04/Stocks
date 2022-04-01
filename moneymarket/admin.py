from django.contrib import admin
from .models import  Stock,my_stocks
# Register your models here.
admin.site.register(Stock)
admin.site.register(my_stocks)