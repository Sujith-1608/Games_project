from django.urls import path
from .import views

urlpatterns=[
    path('',views.home,name='home'),
    path('guess_number/',views.guess_number,name='guess_number'),
    path('guess_word/',views.guess_word,name='guess_word'),
    path('number_21/',views.number_21,name='21_number'),
    ]