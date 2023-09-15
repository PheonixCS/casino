from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFit
from imagekit.models import ImageSpecField
import random
import string
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
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    def save(self, *args, **kwargs):
        if not self.referral_code:
            self.referral_code = self.generate_unique_referral_code()
        super().save(*args, **kwargs)
    def generate_unique_referral_code(self):
        code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
        while User.objects.filter(referral_code=code).exists():
            code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
        return code
class Referral(models.Model):
    referrer = models.ForeignKey(User, on_delete=models.CASCADE)
    referred_user = models.ForeignKey(User, related_name='referrals', on_delete=models.CASCADE)