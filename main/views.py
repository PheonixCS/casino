from django.shortcuts import render, redirect
from .models import Game
from .models import Stock
from .models import User
from .models import Referral
from django.contrib.auth import authenticate, login, logout
import random

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
def part(request):
    if request.user.is_authenticated:
        user = request.user
        referrals = Referral.objects.filter(referrer=user)
        referral_code = user.referral_code
        context = {
            'referrals': referrals,
            'referral_code': referral_code,
            'user': user
        }
        return render(request, 'main/partnerProgramMain.html', context)
    return render(request, 'main/partnerProgramMain.html')
def register_user(request):
    if request.method == 'POST':
        phone_number = request.POST.get('regPhone')
        referral_code = request.POST.get('referralCode')
        user = User.objects.create_user(username=phone_number, password='')
        user = authenticate(username=phone_number, password='')
        if referral_code:
            try:
                referrer = User.objects.get(referral_code=referral_code)
                referral = Referral(referrer=referrer, referred_user=user)
                referral.save()
            except User.DoesNotExist:
                # Обработка случая, если реферальный код недействителен
                pass
        # Создание пользователя без пароля
        
        login(request, user)
        # Дополнительная логика обработки после создания пользователя
        return redirect('/')  # Перенаправление на главную страницу после успешной регистрации
    return render(request, 'main/index.html')
def login_view(request):
    if request.method == 'POST':
        phone = request.POST['loginPhone']
        # TODO: проверить введенный номер телефона и выполнить вход на сайт
        # ...
        # пример автоматического входа пользователя
        user = User.objects.get(username=phone)
        login(request, user)
        return redirect('/')  # перенаправление на главную страницу после входа
    return render(request, 'main/index.html')
def logout_view(request):
    logout(request)
    return redirect('/') 