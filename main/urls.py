from django.urls import path
from . import views

urlpatterns = [
    path('',views.index),   
    path('about/', views.about), 
    path('ruls/', views.ruls), 
    path('stocks/', views.stocks, name='stocks'),
    path('register/', views.register_user, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('part/', views.part, name='part'),
    path('accaunt/', views.peAc, name='accaunt'),

		path('slotsInit', views.slots_init, name='slots_init'),
		path('spinRequest', views.spin_request, name='spin_request'),
		path('Slot.php', views.slot_php, name='slot_php')
]
