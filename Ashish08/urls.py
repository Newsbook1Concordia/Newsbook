
from django.urls import include, path

from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('', views.login, name='login'),
    path('news/', views.news, name='news'),
    path('category/',views.category, name='category'),
    path('profile/',views.profile, name='profile'),
    path('news/Business/',views.business, name='business')
    

]