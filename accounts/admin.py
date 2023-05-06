from django.contrib import admin
from .models import City, Contact, Region, User




@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']
    ordering = ['name']




@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ['name', 'region']
    list_filter = ['region']
    search_fields = ['name', 'region']
    ordering = ['name', 'region']




@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'username', 'email', 'is_active', 'is_staff']
    list_filter = ['is_active', 'is_staff']
    search_fields = ['first_name', 'last_name', 'username', 'email']
    ordering = ['last_name', 'first_name', 'username']




@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['user', 'region', 'city', 'address', 'phone']
    search_fields = ['user', 'region', 'city']
    search_fields = ['user', 'region', 'city']
    ordering = ['user', 'region', 'city']