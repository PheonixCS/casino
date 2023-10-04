from django.shortcuts import render, redirect
from .models import Game
from .models import Stock
from .models import User
from .models import Referral
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
import requests

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



def slots_init(request):
		token = request.GET.get('token')
		login_hash = request.GET.get('hash')
		
		# получаем из БД
		balance = 100000.0
		scheme_handle = "Scheme"  # Пример значения из файла 
		
		response_data = {
				'balance': balance,
				'handle': scheme_handle,
		}
		return JsonResponse(response_data)

def spin_request(request):
	token = request.GET.get('token')
	bet = int(request.GET.get('bet'))
	lines = [int(line) for line in request.GET.get('lines').split(',')]
	free_spin_count = 0
	limit = -1.0
	response_data = {
			'freeSpinCount': free_spin_count,
			'bet': bet,
			'limit': limit,
			'balance': 100000.0,  # Пример значения баланса игрока
			'handle': 'Scheme',  # Пример значения из файла Scheme.json
			'lines': lines,
	}
	response = requests.post('http://your-domain.com/path/to/Slot.php', json=response_data)
	# Проверка наличия ошибки в JSON-ответе
	if 'error' in response.json():
			# Обработка ошибки
			return JsonResponse({'error': 'An error occurred'})
		# Извлечение данных из JSON-ответа
	balance = response.json().get('balance')
	total_win = response.json().get('totalWin')
	free_spin_count = response.json().get('freeSpinCount')
	

	connect_response = {
		'balance': balance,
		'totalWin': total_win,
		'bet': bet,
		'window': response.json().get('window'),
		'special': response.json().get('special'),
		'lines': response.json().get('lines'),
		'complex': response.json().get('complex'),
		'freeSpin': response.json().get('freeSpin'),
		'bonus': response.json().get('bonus'),
		'freeSpinCount': free_spin_count,
	}
	return JsonResponse(connect_response)

def slot_php(request):
	# Получение JSON-ответа от spin_request
	json_data = request.body.decode('utf-8')
	response = requests.post('http://your-domain.com/path/to/Slot.php', data=json_data)
	if response.status_code == 200:
		# Парсинг JSON-ответа
		response_data = response.json()
		# Возвращение JSON-ответа в качестве ответа Django
		return JsonResponse(response_data)
	else:
		# Обработка ошибки, если ответ от Slot.php не был успешным
		return JsonResponse({'error': 'An error occurred'})