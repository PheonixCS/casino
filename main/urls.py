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

	path("get_token/", views.get_token, name="get_token"),
	path("run_game/", views.run_game, name="run_game"),
	path("slotsInit/", views.slots_init),
	
	path("spinRequest/", views.spin_request),
	path("takeRequest/", views.take_request),
	path("doubleRequest/", views.double_request),
	path('update_balance/', views.update_balance, name='update_balance'),
]
