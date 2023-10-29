from django.contrib import admin
from .models import Game
from .models import Stock
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User
from .models import Balance
from .models import Referral
from .models import GlobalSettings
# Register your models here.

admin.site.register(Game)
admin.site.register(Stock)

class CustomUserAdmin(UserAdmin):
	list_display = ("username", "email", "avatar_thumbnail", "token")
	fieldsets = (
			(None, {'fields': ('username', 'password')}),
			('Personal Info', {'fields': ('first_name', 'last_name', 'email', 'avatar')}),
			#('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
			#('Important dates', {'fields': ('last_login', 'date_joined')}),
			('balance',{'fields':('balance',)}),
			('freeSpinCount',{'fields':('freeSpinCount',)})
	)
@admin.register(Balance)
class BalanceAdmin(admin.ModelAdmin):
	list_display = ("id", "ProfitBal", "CyclBal")
	pass
admin.site.register(User, CustomUserAdmin)


class ReferralAdmin(admin.ModelAdmin):
    list_display = ['referrer', 'referred_user','stonks']
    list_filter = ['referrer', 'referred_user']
    search_fields = ['referrer__username', 'referred_user__username']
    list_per_page = 20
admin.site.register(Referral, ReferralAdmin)


class GlobalSettingsAdmin(admin.ModelAdmin):
    list_display = ['id','PerRef', 'PerReturn']
admin.site.register(GlobalSettings, GlobalSettingsAdmin)