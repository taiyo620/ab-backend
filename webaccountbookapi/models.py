from django.db import models
from django.core.files import File
import datetime
import os
from .storage import OverwriteStorage
from django.contrib.auth.models import User,AbstractBaseUser
from django.contrib.auth.base_user import base_userManager
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings

# Create your models here.
class Genre(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    genre_name = models.CharField(max_length=100)

    def __str__(self):
        return self.genre_name

class Purchase(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    genre = models.ForeignKey(Genre,on_delete=models.CASCADE)
    price = models.IntegerField(default=0)
    purchase_date = models.DateField(auto_now=False,default=datetime.date.today)

    def __str__(self):
        return self.name


class Siteuser(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="siteuser")
    monthly_budget = models.IntegerField(default=50000)

    @receiver(post_save,sender=settings.AUTH_USER_MODEL)
    def create_site_user(sender,instance,created,**kwargs):
        if created:
            Siteuser.objects.create(user=instance)

    @receiver(post_save,sender=settings.AUTH_USER_MODEL)
    def save_site_user(sender,instance,**kwargs):
        instance.siteuser.save()

class Graphs(models.Model):
    graph = models.ImageField(upload_to='images/',blank=True,storage=OverwriteStorage())
