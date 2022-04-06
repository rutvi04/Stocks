from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Profile(models.Model):
    #user = models.OneToOneField(User, related_name='uid', on_delete=models.CASCADE)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # name = models.CharField(max_length=50)
    UID = models.CharField(primary_key='True', max_length=15)
    # email = models.EmailField(blank='False')
    # pwd = models.CharField(max_length=100)
    idProof = models.ImageField(upload_to='Logos/Client_ID', null='True')
    DOB = models.DateField(null='True')
    address = models.TextField(null='True')
    available_bal = models.PositiveIntegerField(default=0)
    invested_bal = models.PositiveIntegerField(default=0)
    demat_ac = models.IntegerField()
    bank_ac = models.IntegerField()
    gender_choices = [('M', "Male"), ('F', 'Female'), ('O', 'Prefer not to say')]
    gender = models.CharField(max_length=1, choices=gender_choices, default='M')

    def __str__(self):
        return str(self.user)

    def save(self):
        super().save()

class Stock(models.Model):
    ticker = models.CharField(max_length=10)
    author = models.ForeignKey(User, related_name='uid_stock', on_delete=models.CASCADE, default=None)

    def __str__(self):
        return self.ticker

class my_stocks(models.Model):
    stock_symbol= models.CharField(max_length=50)
    quantity = models.PositiveIntegerField(default=0, blank= False)
    my_author = models.ForeignKey(User, related_name='uid_my_stock', on_delete=models.CASCADE, default=None)
    price = models.DecimalField(default=0,max_digits=6, decimal_places=2)
    date = models.DateTimeField(auto_now=True)
