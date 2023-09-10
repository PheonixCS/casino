from django.shortcuts import render, get_object_or_404
from .models import Game
from .models import Stock

def index(request):
	#return HttpResponse("<h4>test</h4>");
	games = Game.objects.all()
	return render(request, 'main/index.html', {'games': games})
# здесь переписать получаемые объекты на акции
def stocks(request):
    stocks = Stock.objects.all()
    return render(request, 'main/stocks.html', {'stocks': stocks})
def about(request):
	return render(request,'main/about.html')
def ruls(request):
	return render(request,'main/ruls.html')
