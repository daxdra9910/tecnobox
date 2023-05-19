from django.contrib import admin
from django.utils.html import format_html

from apps.utils.actions import BaseModelAdmin, disable_selected, enable_selected
from apps.shop.models import Review




@admin.register(Review)
class ReviewAdmin(BaseModelAdmin):
    """
    Modelo Review de la interfaz de administración.
    """
    list_display = ['user', 'product', 'render_stars', 'comment', 'created_at', 'is_active']
    list_filter = ['rating']
    search_fields = ['user', 'product', 'is_active']
    ordering = ['user', 'product', 'rating']
    actions = [disable_selected, enable_selected]


    def render_stars(self, obj):
        filled_stars = int(obj.rating)
        empty_stars = 5 - filled_stars
        stars_html = '<span class="text-warning">' + '★' * filled_stars + '☆' * empty_stars + '</span>'
        return format_html(stars_html)


    render_stars.short_description = 'Puntaje'