from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, AccountTier


@admin.register(AccountTier)
class AccountTierAdmin(admin.ModelAdmin):
    list_display = ('name', 'thumbnail_sizes', 'originally_uploaded_image', 'generate_exp_links')
    list_filter = ('originally_uploaded_image', 'generate_exp_links')


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'is_staff', 'account_tier')
    list_filter = ('is_staff', 'account_tier')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'account_tier')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )



#
# admin.site.register(CustomUser, CustomUserAdmin)
