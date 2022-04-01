from django.db import models

# Create your models here.
class Stock(models.Model):
    ticker = models.CharField(max_length=10)

    def __str__(self):
        return self.ticker

class my_stocks(models.Model):
    stock_symbol= models.TextField()
    quantity = models.PositiveIntegerField(default=0, blank= False)




