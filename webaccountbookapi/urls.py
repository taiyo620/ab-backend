from django.urls import path,re_path

from . import views

app_name = "webaccountbookapi"

urlpatterns = [
    path('',views.index,name='index'),
    path('add_purchase/',views.add_purchase,name="add_purchase"),
    path('<int:purchase_id>/delete',views.delete_purchase,name="delete_purchase"),
    path('genre/add/',views.add_genre,name="add_genre"),
    path('genre/<int:genre_id>/delete/',views.delete_genre,name="delete_genre"),
]
