from django.shortcuts import render
from django.http import HttpResponse
from .models import Game

def index(request):
	#return HttpResponse("<h4>test</h4>");
	games = Game.objects.all()
	return render(request, 'main/index.html', {'games': games});
def about(request):
	return render(request,'main/about.html');
def ruls(request):
	return render(request,'main/ruls.html');
# Create your views here.
