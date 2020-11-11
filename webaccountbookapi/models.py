from django.db import models
from django.core.files import File
import urllib
import os
from .storage import OverwriteStorage

# Create your models here.

class Genre(models.Model):
    genre_name = models.CharField(max_length=100)

    def __str__(self):
        return self.genre_name

class User(models.Model):
    user_name = models.CharField(max_length=100)

    def __str__(self):
        return self.user_name

class Purchase(models.Model):
    name = models.CharField(max_length=100)
    genre = models.ForeignKey(Genre,on_delete=models.CASCADE)
    price = models.IntegerField(default=0)
    purchase_date = models.DateField(auto_now=False)

    def __str__(self):
        return self.name

class Graphs(models.Model):
    graph = models.ImageField(upload_to='images/',blank=True,storage=OverwriteStorage())
