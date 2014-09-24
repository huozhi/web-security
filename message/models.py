from django.db import models
import datetime

# Create your models here.

class Message(models.Model):
    date = models.DateTimeField('date published')
    content = models.CharField(max_length=200)