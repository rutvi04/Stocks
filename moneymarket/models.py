from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Stock(models.Model):
    ticker = models.CharField(max_length=10)

    def __str__(self):
        return self.ticker

class my_stocks(models.Model):
    stock_symbol= models.TextField()
    quantity = models.PositiveIntegerField(default=0, blank= False)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # name = models.CharField(max_length=50)
    UID = models.CharField(primary_key='True', max_length=15)
    # email = models.EmailField(blank='False')
    # pwd = models.CharField(max_length=100)
    # idProof = models.ImageField(upload_to='Logos/Client_ID')
   # DOB = models.DateField()
    address = models.TextField(null='True')
    available_bal = models.PositiveIntegerField(default=0)
    invested_bal = models.PositiveIntegerField(default=0)
    demat_ac = models.IntegerField()
    bank_ac = models.IntegerField()
    gender_choices = [('M', "Male"), ('F', 'Female'), ('O', 'Prefer not to say')]
    gender = models.CharField(max_length=1, choices=gender_choices, default='M')

    def __str__(self):
        return str(self.user)




