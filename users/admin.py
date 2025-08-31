from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('username', 'email', 'is_seller', 'is_buyer', 'is_staff', 'is_active', 'date_joined')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    ordering = ('username',)
    
    # Add custom fields to the fieldsets
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('phone_number', 'is_seller', 'is_buyer', 'profile_image')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('phone_number', 'is_seller', 'is_buyer', 'profile_image')}),
    )

admin.site.register(CustomUser, CustomUserAdmin)
