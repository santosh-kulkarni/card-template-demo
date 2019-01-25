from django.contrib import admin
from django.urls import path, include
from . import views


urlpatterns = [
    path("putdata/", views.put_data,),
    path('', views.first_page, ),
]
