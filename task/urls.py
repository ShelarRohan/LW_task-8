from django.contrib import admin
from django.urls import path
from . import views
# from .views import index
from django.contrib.auth import views as auth_views 
urlpatterns = [
    path('index',views.index,name="index"),
    path('getinfo/',views.get,name="getinfo"),
    
    path('confirmation/', views.confirmation, name = 'confirmation'),
    path('error/', views.error, name = 'error'),

]
