from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse,reverse_lazy
from django.shortcuts import render,get_object_or_404
from django.conf import settings
from django.core.files import File
from django.views.generic.edit import CreateView

from .forms import PurchaseForm,GenreForm,SignUpForm
from .models import Purchase,Genre,Graphs
from django.utils import timezone
from django_pandas.io import read_frame
from django.db import connection
import matplotlib.pyplot as plt
import japanize_matplotlib
import os

from django.contrib.auth import login,logout
from django.contrib.auth.views import LoginView
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

import locale
locale.setlocale(locale.LC_ALL, '')


# Create your views here.
@login_required
def index(request):
    user = User.objects.get(username=str(request.user))
    genre_list = Genre.objects.filter(author=user)
    if not genre_list:
        Genre.objects.create(author=user,genre_name="食費")
        Genre.objects.create(author=user,genre_name="交通費")
        Genre.objects.create(author=user,genre_name="被服費")
        Genre.objects.create(author=user,genre_name="交際費")
        Genre.objects.create(author=user,genre_name="雑貨費")
        genre_list = Genre.objects.filter(author=user)

    purchase_list = Purchase.objects.filter(author=user.id)
    purchase_form = PurchaseForm(label_suffix='')
    purchase_form.fields['genre'].queryset = genre_list
    genre_form = GenreForm(label_suffix='')


    now = timezone.now()
    this_month_purchase_list = purchase_list.filter(purchase_date__year=now.year).filter(purchase_date__month=now.month)
    this_month_purchase_list = this_month_purchase_list.order_by('purchase_date')
    sum_price = sum([purchase.price for purchase in this_month_purchase_list])

    Graphs.objects.all().delete()
    with connection.cursor() as cursor:
        cursor.execute('alter table webaccountbookapi_graphs auto_increment = 1')

    message = request.session.get('message','')

    params = {
    "purchase_list": purchase_list,
    "purchase_form": purchase_form,
    "genre_form": genre_form,
    "genre_list": genre_list,
    "this_month": now.strftime("%Y年%m月"),
    "this_month_purchase_list": this_month_purchase_list,
    "sum_price": sum_price,
    "message": message,
    }
    if this_month_purchase_list:
        this_month_purchase_df = read_frame(this_month_purchase_list)
        genre_proportion = this_month_purchase_df.groupby(by="genre").sum().sort_values("price",ascending=False)
        colors = ["#2dedc7","#B3FB30","#EF2D56","#FF8230","#0EA486","#7CBD03","#A50D2E","#C64C00"]
        genre_proportion['price'].plot(fontsize=13,ylabel="",kind="pie",startangle=90,wedgeprops={'linewidth':3,'edgecolor':'white'},counterclock=False,colors=colors)
        plt.title("")
        file_name = "graph" + user.username + ".jpg"
        image_url = os.path.join(settings.MEDIA_ROOT,file_name)

        plt.savefig(image_url)
        pi_graph = Graphs()
        im = open(image_url,"rb")
        pi_graph.graph.save(file_name,im,save=True)
        im.close()
        plt.clf()
        plt.close()

        params['graph'] = pi_graph

    return render(request,"webaccountbookapi/index.html",params)


def add_purchase(request):
    user = User.objects.get(username=str(request.user))
    if request.method == 'POST':
        form = PurchaseForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            genre = form.cleaned_data['genre']
            price = form.cleaned_data['price']
            purchase_date = form.cleaned_data['purchase_date']
            Purchase.objects.create(author=user,name=name,genre=genre,price=price,purchase_date=purchase_date)
            request.session['message'] = "家計簿に追加されました"
        else:
            request.session['message'] = "入力に不備があります"

    return HttpResponseRedirect(reverse('webaccountbookapi:index'))

def delete_purchase(request,purchase_id):
    del_purchse = get_object_or_404(Purchase,pk=purchase_id)
    request.session['message'] = f'{del_genre.name}を削除しました'
    del_purchse.delete()

    return HttpResponseRedirect(reverse('webaccountbookapi:index'))

def add_genre(request):
    user = User.objects.get(username=str(request.user))
    if request.method == 'POST':
        form = GenreForm(request.POST)
        if form.is_valid():
            genre_name= form.cleaned_data['genre_name']
            Genre.objects.create(author=user,genre_name=genre_name)
            request.session['message']="ジャンルが追加されました"
        else:
            request.session['message']="ジャンル名を記入してください"

    return HttpResponseRedirect(reverse('webaccountbookapi:index'))


def delete_genre(request,genre_id):
    del_genre = get_object_or_404(Genre,pk=genre_id)
    request.session['message'] = f'ジャンル  {del_genre.genre_name}  を削除しました'
    del_genre.delete()

    return HttpResponseRedirect(reverse('webaccountbookapi:index'))

class SignUp(CreateView):
    form_class = SignUpForm
    template_name = 'webaccountbookapi/create.html'
    success_url = reverse_lazy('webaccountbookapi:index')

    def form_valid(self,form):
        user = form.save()
        login(self.request,user)
        self.object = user
        return HttpResponseRedirect(self.get_success_url())

class login_to_index(LoginView):
    template_name='webaccountbookapi/login.html'
    redirect_field_name = 'webaccountbookapi:index'

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('webaccountbookapi:index'))
