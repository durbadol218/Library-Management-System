from django.db import models
from librarians.models import UserProfile
from .constants import TRANSACTION_TYPE
# Create your models here.

# Akta User Deposit, Withdraw, Loan agula korte paarbe!

class TransactionModel(models.Model):
    # akjon user er multiple type transactions hoite paare!
    account = models.ForeignKey(UserProfile, related_name='transactions', on_delete=models.CASCADE)
    amount = models.DecimalField(decimal_places=2, max_digits=15)
    balance_after_transaction = models.DecimalField(decimal_places=2, max_digits=15, null=True)
    transaction_type = models.IntegerField(choices=TRANSACTION_TYPE, null= True)
    timestamp = models.DateTimeField(auto_now_add=True)