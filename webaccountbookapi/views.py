from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse,reverse_lazy
from django.shortcuts import render,get_object_or_404
from django.views.generic.edit import CreateView
from django.utils import timezone

from .forms import PurchaseForm,GenreForm,SignUpForm,SiteuserForm,AuthenticationFormWithoutPassword
from .models import Purchase,Genre,Siteuser,NameOnlyUser
from .graphs import make_pi
from django_pandas.io import read_frame
import os

from django.contrib.auth import login,logout
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required

import locale
locale.setlocale(locale.LC_ALL, '')


# Create your views here.
@login_required
def index(request):
    user = request.user
    monthly_budget = user.siteuser.monthly_budget

    if not Genre.objects.bind_user(user):
        for default_genre in ['食費','交通費','交際費','被服費','雑貨費']:
            Genre.objects.create(author=user,genre_name=default_genre)
    genre_list = Genre.objects.bind_user(user)

    purchase_list = Purchase.objects.bind_user(user)
    purchase_form = PurchaseForm(label_suffix='')
    purchase_form.fields['genre'].queryset = genre_list
    genre_form = GenreForm(label_suffix='')
    site_user_form = SiteuserForm(instance=user.siteuser)

    this_month_purchase_list = purchase_list.thismonth()
    sum_price = sum([purchase.price for purchase in this_month_purchase_list])
    message = request.session.get('message','')


    params = {
    "purchase_list": purchase_list,
    "purchase_form": purchase_form,
    "genre_form": genre_form,
    "genre_list": genre_list,
    "this_month": timezone.now().strftime("%Y年%m月"),
    "this_month_purchase_list": this_month_purchase_list,
    "sum_price": sum_price,
    "message": message,
    "site_user_form": site_user_form,
    "rest_budget": monthly_budget - sum_price,
    }
    if this_month_purchase_list:
        this_month_purchase_df = read_frame(this_month_purchase_list)
        genre_proportion = this_month_purchase_df.groupby(by="genre").sum().sort_values("price",ascending=False)
        file_name = "graph" + user.username + ".jpg"
        params['graph'] = make_pi(genre_proportion["price"],file_name)

    return render(request,"webaccountbookapi/index.html",params)

@login_required
def update_budget(request):
    user = request.user
    if request.method == "POST":
        form = SiteuserForm(request.POST)
        if form.is_valid():
            monthly_budget = form.cleaned_data['monthly_budget']
        user.siteuser.monthly_budget = monthly_budget
        user.siteuser.save()
    return HttpResponseRedirect(reverse('webaccountbookapi:index'))


def add_purchase(request):
    user = request.user
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
    user = request.user
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
        login(self.request,user,backend='webaccountbookapi.backends.MyBackend')
        self.object = user
        return HttpResponseRedirect(self.get_success_url())


class login_to_index(LoginView):
    form_class = AuthenticationFormWithoutPassword
    template_name='webaccountbookapi/login.html'
    redirect_field_name = 'webaccountbookapi:index'

    def form_valid(self, form):
        username = form.cleaned_data['username']
        login(self.request, NameOnlyUser.objects.get(username=username),backend='webaccountbookapi.backends.MyBackend')
        return HttpResponseRedirect(self.get_success_url())


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('webaccountbookapi:index'))
