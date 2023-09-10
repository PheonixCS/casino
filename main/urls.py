from django.urls import path
from . import views

urlpatterns = [
    path('',views.index),   
    path('about/', views.about), 
    path('ruls/', views.ruls), 
    path('stocks/', views.stocks, name='stocks'),
]
