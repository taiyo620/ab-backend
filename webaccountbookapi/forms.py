from django import forms
from django.utils import timezone

from .models import Purchase,Genre
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class PurchaseForm(forms.ModelForm):
    class Meta:
        model = Purchase
        fields = ['name','genre','price','purchase_date']
        labels = {
            'name':'名前',
            'genre':'ジャンル',
            'price':'価格',
            'purchase_date':'購入日',
        }
        widgets = {
            'purchase_date': forms.SelectDateWidget(years=[x for x in range(timezone.now().year - 1,timezone.now().year + 1)]),
        }
        label_suffix = ''



class GenreForm(forms.ModelForm):
    class Meta:
        model = Genre
        fields = ['genre_name',]
        labels = {
            'genre_name':"ジャンル名"
        }

class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username','password1')
