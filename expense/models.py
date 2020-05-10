from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils import timezone
from decimal import Decimal
from datetime import datetime


class Category(models.Model):
	name = models.CharField(max_length=50)

	def __str__(self):
		return "{}".format(self.name)

class Transaction(models.Model):
    category = models.ForeignKey(Category, blank=True, null=True, on_delete=models.SET_NULL)
    value = models.DecimalField(default=Decimal(0.0), decimal_places=2, max_digits=64)
    memo = models.CharField(max_length=1000, blank=True, default="")
    date = models.DateField(default=timezone.now) 
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,null=True)
    
    def __str__(self):
        return "Transaction by {} on {}".format(self.user, self.date)
