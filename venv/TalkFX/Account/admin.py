from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from Account.models import Account

# Register your models here.

class AccountAdmin(UserAdmin):
    list_display = ('email','username','date_joined', 'last_login', 'is_admin','is_staff')
    search_fields = ('email','username')
    readonly_fields=('date_joined', 'last_login')
    list_filter = ('is_staff', 'is_admin', 'is_superuser')	
    filter_horizontal = ()
    fieldsets = ()


admin.site.register(Account, AccountAdmin)