from django.db import models
from django.contrib.auth.models import User
from .constants import GENDER
# django amaderke builtin user make korar facility dey!

class UserProfile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name="account")
    birth_date = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=50,choices=GENDER)
    balance = models.DecimalField(default=0, max_digits=12, decimal_places=2)
    city = models.CharField(max_length=100)
    postal_code = models.IntegerField()
    country = models.CharField(max_length=255)
    def __str__(self):
        return f"{self.user.username}"