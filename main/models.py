from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFit
from imagekit.models import ImageSpecField
import random
import string
import hashlib
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from datetime import date
# Create your models here.

# здесь добавить акции
class Game(models.Model):
	GameName = models.CharField(max_length=255)
	lastRun = models.DateTimeField(null=True, blank=True)
	countRun = models.IntegerField(null=True, blank=True)
	gamePath = models.CharField(max_length=255, null=True, blank=True)
	gamePathDemo = models.CharField(max_length=255, null=True, blank=True)
	icoPath = models.ImageField(upload_to='media/gameImg_images/')
	def __str__(self):
			return self.GameName

class Stock(models.Model):
	name = models.CharField(max_length=100)
	description = models.TextField()
	time = models.DateTimeField()
	path_to_img = models.ImageField(upload_to='media/stock_images/')
	def __str__(self):
			return self.name

class Avatar(models.Model):
	image = models.ImageField(upload_to='avatars/')
	def __str__(self):
			return self.image.name
    
class User(AbstractUser):
	groups = models.ManyToManyField(Group, related_name='main_users')
	user_permissions = models.ManyToManyField(Permission, related_name='main_users_permissions')
	avatar = ProcessedImageField(upload_to='avatars/', processors=[ResizeToFit(300, 300)], format='JPEG', options={'quality': 90}, default='avatars/1s.png')
	avatar_thumbnail = ImageSpecField(source='avatar', processors=[ResizeToFit(50, 50)], format='JPEG', options={'quality': 90})
	STATUS_CHOICES = (
			(1, 'Статус 1'),
			(2, 'Статус 2'),
			(3, 'Статус 3'),
			(4, 'Статус 4'),
			(5, 'Статус 5'),
	)
	status = models.IntegerField(choices=STATUS_CHOICES, default=1)
	referral_code = models.CharField(max_length=10, unique=True, blank=True, null=True)
	points = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
	balance = models.FloatField(max_length=10, default=0.00)
	lastTotalWin = models.FloatField(max_length=10, default=0.00)
	freeSpinCount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

	bet = models.FloatField(max_length=10, default=0.00)
	step = models.IntegerField(choices=STATUS_CHOICES, default=1)
	stepBalance = models.FloatField(max_length=10, default=0.00)

	token = models.CharField(max_length=32, blank=True, null=True)
	def save(self, *args, **kwargs):
			if not self.referral_code:
					self.referral_code = self.generate_unique_referral_code()
			if not self.token:
				self.token = hashlib.md5(self.username.encode()).hexdigest()
			super().save(*args, **kwargs)
	def generate_unique_referral_code(self):
			code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
			while User.objects.filter(referral_code=code).exists():
					code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
			return code
	def update_avatar(self):
		if self.status == 1:
				self.avatar = 'avatars/1s.png'
		elif self.status == 2:
				self.avatar = 'avatars/2s.png'
		elif self.status == 3:
				self.avatar = 'avatars/3s.png'
		elif self.status == 4:
				self.avatar = 'avatars/4s.png'
		elif self.status == 5:
				self.avatar = 'avatars/5s.png'
		self.save()
@receiver(post_save, sender=User)
def update_avatar(sender, instance, created, **kwargs):
	if created:
			instance.update_avatar()
class DailyDeposit(models.Model):
	user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
	deposit_date = models.DateField(default=date.today)
	amount = models.FloatField(default=0.0)
	def __str__(self):
			return f'{self.user} - {self.deposit_date}'
	class Meta:
			verbose_name = 'Ежедневное пополнение'
			verbose_name_plural = 'Ежедневные пополнения'

class Referral(models.Model):
	referrer = models.ForeignKey(User, on_delete=models.CASCADE)
	referred_user = models.ForeignKey(User, related_name='referrals', on_delete=models.CASCADE)
	stonks = models.FloatField(max_length=10, default=0.00)

class Payment(models.Model):
	amount = models.DecimalField(max_digits=10, decimal_places=2)
	payment_method = models.CharField(max_length=100)
	status = models.CharField(max_length=100)
	date = models.DateTimeField(auto_now_add=True)
	def __str__(self):
			return f"Payment #{self.pk}"
class Balance(models.Model):
	id = models.AutoField(primary_key=True)
	ProfitBal = models.FloatField(max_length=10)
	CyclBal = models.FloatField(max_length=10)

class GlobalSettings(models.Model):
	id = models.AutoField(primary_key=True)
	PerRef = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Процент прибыли с рефералов')
	PerReturn = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Общий процент отдачи')
	def __str__(self):
			return f'Настройки #{self.pk}'
	class Meta:
			verbose_name_plural = 'Настройки'

class ActivatedStock(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
	is_active = models.BooleanField(default=True)
	def __str__(self):
			return self.stock.name