from django.shortcuts import render, redirect
from .models import Game
from .models import Stock
from .models import User
from .models import Referral
from .models import Balance
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
import requests
from django.http import HttpResponse
from urllib.parse import urlencode
import hashlib
import base64
from datetime import datetime

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
def peAc(request):
    if request.user.is_authenticated:
        user = request.user
        if user.status < 4:
             nextST = user.status+1
        else:
             nextST = "max"
        context = {
            'nextST' : nextST,
            'user': user
        }
        return render(request,'main/peAc.html', context)
    else:
        return render(request,'/') 
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

def get_token(request):
	# Ваша логика для получения токена
	# если пользователь аутентифицирован
	if request.user.is_authenticated:
			# получаем логин 
			login = request.user.username
			#получаем текущее время
			current_time = datetime.now()
			# получаем токен до хеширования
			token_data = login + str(current_time)
			#хешируем
			token = hashlib.md5(token_data.encode()).hexdigest()
			#перезаписываем в сессии
			request.user.token = token
			#перезаписываем в базе
			request.user.save()
			#возвращаем токен
			return JsonResponse({"token": token})
	#если не аутентифирован то
	#генерируем нулевой токен и возваращаем 0 и ошибку 0
	#ошибка 0 означает что пользователь не аутентифирован
	else:
			token = 0
			return JsonResponse(
					{"token": token, "error": 0}
			)
def run_game(request):
	token = str(request.GET.get("token"))
	path = request.GET.get("path")
	url = f"/static/main/games/{path}/index.html?token={token}"
	return redirect(url)

def slots_init(request):
	#game = request.GET.get("game")
	token = request.GET.get("token")
	user = User.objects.filter(token=token).first()

	if user:
			balance = user.balance
	else:
			# Обработка случая, когда пользователь не найден
			balance = None  # или другое значение по умолчанию

	with open(
			"C:/Projects/casino/static/main/slot_logic/Schemes/Scheme.json",
			"rb",
	) as file:
			scheme_bytes = file.read()
	encoded_scheme = base64.b64encode(scheme_bytes).decode()
	scheme_handle = encoded_scheme  # Пример значения из файла

	response_data = {
			"balance": balance,
			"handle": scheme_handle,
			"token": token,
	}
	return JsonResponse(response_data)

def spin_request(request):
	token = request.GET.get("token")
	bet = request.GET.get("bet")
	lines = [int(line) for line in request.GET.get("lines").split(",")]
	free_spin_count = 0
	# limit = -1.0
	# with open(
	# 		"C:/Projects/casino/static/main/slot_logic/Schemes/Scheme.json",
	# 		"rb",
	# ) as file:
	# 		scheme_bytes = file.read()
	#encoded_scheme = base64.b64encode(scheme_bytes).decode()
	#scheme_handle = encoded_scheme  # Пример значения из файла
	user = User.objects.filter(token=token).first()

	if not Balance.objects.exists():
		Balance.objects.get_or_create(ProfitBal=0, CyclBal=0)

	Bal = Balance.objects.filter(id=1).first()
	limit = Bal.CyclBal
	response_data = {
			"freeSpinCount": free_spin_count,
			"bet": bet,
			"limit": limit,
			"balance": user.balance,  # Пример значения баланса игрока
			"handle": "Scheme",  # Пример значения из файла Scheme.json
			"lines": lines,
			"ignoreSpecial": ["FreeSpin","Bonus"],
			"complex_get": False,
			"wild_ID": -1,
			"winner": False
	}
	response = requests.post(
			"http://127.0.0.1/static/main/slot_logic/slot.php", json=response_data
	)
	#return JsonResponse(response.json())
	# Проверка наличия ошибки в JSON-ответе
	if "error" in response.json():
			# Обработка ошибки
			return JsonResponse({"error": "An error occurred"})
	# Извлечение данных из JSON-ответа
	balance = response.json().get("balance")
	total_win = response.json().get("totalWin")
	free_spin_count = response.json().get("freeSpinCount")
	user.balance = balance
	user.save()
	if total_win:
		Bal.CyclBal -= total_win
		Bal.CyclBal += response.json().get("bet")*0.95
		Bal.ProfitBal += response.json().get("bet")*0.05
	else:
		Bal.CyclBal += response.json().get("bet")*0.95
		Bal.ProfitBal += response.json().get("bet")*0.05
	Bal.save()
	connect_response = {
			"balance": balance,
			"totalWin": total_win,
			"bet": response.json().get("bet"),
			"window": response.json().get("window"),
			"special": response.json().get("special"),
			"lines": response.json().get("lines"),
			"complex": response.json().get("complex"),
			"freeSpin": response.json().get("freeSpin"),
			"bonus": response.json().get("bonus"),
			"freeSpinCount": free_spin_count,
	}
	return JsonResponse(connect_response)

def take_request(request):
	token = request.GET.get("token")
	## проверка на токен
	return JsonResponse({"result":"success"})