from django.conf import settings
from django.contrib import admin
from django.utils.html import format_html

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
    list_display = ['first_name', 'last_name', 'username', 'email', 'is_active', 'is_staff', 'profile_photo']
    list_filter = ['is_active', 'is_staff']
    search_fields = ['first_name', 'last_name', 'username', 'email']
    ordering = ['last_name', 'first_name', 'username']


    def profile_photo(self, obj):
        return format_html('<img src="{}" width="100" height="100" />'.format(obj.get_url_photo()))


    profile_photo.short_description = 'Photo'


    class Media:
        css = {
            'all': (settings.STATIC_URL + 'css/admin.css',)
        }




@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['user', 'region', 'city', 'address', 'phone']
    search_fields = ['user', 'region', 'city']
    search_fields = ['user', 'region', 'city']
    ordering = ['user', 'region', 'city']