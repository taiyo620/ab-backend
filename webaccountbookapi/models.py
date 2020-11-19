from django.db import models
from django.core.files import File
import datetime
import os
from .storage import OverwriteStorage
from django.contrib.auth.models import User,AbstractBaseUser
from django.contrib.auth.base_user import BaseUserManager
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from django.utils import timezone

# Create your models here.
class UserBindQuerySet(models.QuerySet):
    def bind_user(self,user):
        return self.filter(author=user)

    def thismonth(self):
        now = timezone.now()
        return self.filter(purchase_date__year=now.year).filter(purchase_date__month=now.month).order_by('purchase_date')


class Genre(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    genre_name = models.CharField(max_length=100)
    objects = UserBindQuerySet.as_manager()

    def __str__(self):
        return self.genre_name

class Purchase(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    genre = models.ForeignKey(Genre,on_delete=models.CASCADE)
    price = models.IntegerField(default=0)
    purchase_date = models.DateField(auto_now=False,default=datetime.date.today)

    objects = UserBindQuerySet.as_manager()

    def __str__(self):
        return self.name

class NameOnlyUserManager(BaseUserManager):
    def create_user(self,username,password=None):
        if not username:
            raise ValueError('Users must have a username')
        user = self.model(username)
        user.save(using=self._db)
        return user

class NameOnlyUser(AbstractBaseUser):
    username = models.CharField(max_length=20,unique=True)
    USERNAME_FIELD = 'username'
    objects = NameOnlyUserManager()



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
