from django.urls import path,re_path

from . import views

app_name = "webaccountbookapi"

urlpatterns = [
    path('create/',views.SignUp.as_view(),name='create'),
    path('login/',views.login_to_index.as_view(),name='login'),
    path('logout/',views.logout_view,name='logout'),
    path('',views.index,name='index'),
    path('add_purchase/',views.add_purchase,name="add_purchase"),
    path('<int:purchase_id>/delete',views.delete_purchase,name="delete_purchase"),
    path('genre/add/',views.add_genre,name="add_genre"),
    path('genre/<int:genre_id>/delete/',views.delete_genre,name="delete_genre"),
]
