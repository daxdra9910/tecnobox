from django.contrib import admin

from apps.utils.actions import BaseModelAdmin, disable_selected, enable_selected
from apps.accounts.models import Contact




@admin.register(Contact)
class ContactAdmin(BaseModelAdmin):
    """
    Modelo Contact de la interfaz de administración.
    """
    list_display = ['user', 'region', 'city', 'address', 'phone', 'created_at', 'updated_at', 'is_active']
    list_filter = ['region', 'city', 'is_active']
    search_fields = ['user', 'region', 'city']
    ordering = ['user', 'region', 'city']
    actions = [disable_selected, enable_selected]