from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index),
    path('announcements', views.announcements),
    path('about', views.about),
]