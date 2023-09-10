from django.db import models

# Create your models here.

# здесь добавить акции
class Game(models.Model):
        GameName = models.CharField(max_length=255)
        lastRun = models.DateTimeField(null=True, blank=True)
        countRun = models.IntegerField(null=True, blank=True)
        gamePath = models.CharField(max_length=255, null=True, blank=True)
        gamePathDemo = models.CharField(max_length=255, null=True, blank=True)
        icoPath = models.CharField(max_length=255, null=True, blank=True)
        def __str__(self):
            return self.GameName

class Stock(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    time = models.DateTimeField()
    path_to_img = models.ImageField(upload_to='media/stock_images/')
