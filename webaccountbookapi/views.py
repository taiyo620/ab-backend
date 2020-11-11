from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render,get_object_or_404
from django.conf import settings
from django.core.files import File

from .forms import PurchaseForm,GenreForm,UserForm
from .models import Purchase,Genre,Graphs,User
from django.utils import timezone
from django_pandas.io import read_frame
from django.db import connection
import matplotlib.pyplot as plt
import os

import locale
locale.setlocale(locale.LC_ALL, '')

message=""
# Create your views here.
def login(request):
    user_form = UserForm(label_suffix='')
    params = {
    'user_form':user_form,
    }
    return render(request,'webaccountbookapi/login.html',params)

def index(request):
    purchase_form = PurchaseForm(label_suffix='')
    genre_form = GenreForm(label_suffix='')
    purchase_list = Purchase.objects.all()
    genre_list = Genre.objects.all()

    now = timezone.now()
    this_month_purchase_list = purchase_list.filter(purchase_date__year=now.year).filter(purchase_date__month=now.month)
    this_month_purchase_list = this_month_purchase_list.order_by('purchase_date')
    sum_price = sum([purchase.price for purchase in this_month_purchase_list])

    Graphs.objects.all().delete()
    with connection.cursor() as cursor:
        cursor.execute('alter table webaccountbookapi_graphs auto_increment = 1')

    this_month_purchase_df = read_frame(this_month_purchase_list)
    genre_proportion = this_month_purchase_df.groupby(by="genre").sum()
    genre_proportion['price'].plot(kind="pie")
    file_name = "graph11.jpg"
    image_url = os.path.join(settings.MEDIA_ROOT,file_name)

    plt.savefig(image_url)
    pi_graph = Graphs()
    im = open(image_url,"rb")
    pi_graph.graph.save(file_name,im,save=True)
    im.close()

    params = {
    "purchase_list": purchase_list,
    "purchase_form": purchase_form,
    "genre_form": genre_form,
    "genre_list": genre_list,
    "this_month": now.strftime("%Y年%m月"),
    "this_month_purchase_list": this_month_purchase_list,
    "sum_price": sum_price,
    "message": message,
    "graph": pi_graph,
    }
    return render(request,"webaccountbookapi/index.html",params)


def add_purchase(request):

    if request.method == 'POST':
        global message
        form = PurchaseForm(request.POST)
        if form.is_valid():
            form.save()
            message = "家計簿に追加されました"
        else:
            message = "入力に不備があります"

    return HttpResponseRedirect(reverse('webaccountbookapi:index'))

def delete_purchase(request,purchase_id):
    del_purchse = get_object_or_404(Purchase,pk=purchase_id)
    message = f'{del_genre.name}を削除しました'
    del_purchse.delete()

    return HttpResponseRedirect(reverse('webaccountbookapi:index'))

def add_genre(request):
    global message
    if request.method == 'POST':
        form = GenreForm(request.POST)
        if form.is_valid():
            form.save()
            message="ジャンルが追加されました"
        else:
            message="ジャンル名を記入してください"

    return HttpResponseRedirect(reverse('webaccountbookapi:index'))


def delete_genre(request,genre_id):
    global message
    del_genre = get_object_or_404(Genre,pk=genre_id)
    message = f'ジャンル  {del_genre.genre_name}  を削除しました'
    del_genre.delete()

    return HttpResponseRedirect(reverse('webaccountbookapi:index'))
