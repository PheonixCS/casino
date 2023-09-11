from asyncio import AbstractServer
from email.headerregistry import Group
from django.contrib import admin
from .models import Game
from .models import Stock
from django.db import models
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User
from imagekit.processors import ResizeToFit
from imagekit.models import ImageSpecField, ProcessedImageField
# Register your models here.

admin.site.register(Game)
admin.site.register(Stock)

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'avatar_thumbnail')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'email', 'avatar')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
admin.site.register(User, CustomUserAdmin)