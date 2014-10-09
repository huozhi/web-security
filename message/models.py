from django.db import models
import datetime

# Create your models here.

class Message(models.Model):
    date = models.DateField(auto_now=True, auto_now_add=True)
    content = models.CharField(max_length=200)