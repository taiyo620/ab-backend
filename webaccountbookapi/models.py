from django.db import models
from django.core.files import File
import datetime
import os
from .storage import OverwriteStorage
from django.contrib.auth.models import User

# Create your models here.
class Genre(models.Model):
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    genre_name = models.CharField(max_length=100)

    def __str__(self):
        return self.genre_name

class Purchase(models.Model):
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    genre = models.ForeignKey(Genre,on_delete=models.CASCADE)
    price = models.IntegerField(default=0)
    purchase_date = models.DateField(auto_now=False,default=datetime.date.today)

    def __str__(self):
        return self.name

class Graphs(models.Model):
    graph = models.ImageField(upload_to='images/',blank=True,storage=OverwriteStorage())
