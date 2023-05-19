from django.contrib import admin
from django.template.loader import render_to_string
from django.utils.html import format_html

from apps.utils.actions import BaseModelAdmin, disable_selected, enable_selected
from apps.shop.models import Product, ProductPhoto




@admin.register(Product)
class ProductAdmin(BaseModelAdmin):
    """
    Modelo Product de la interfaz de administración.
    """
    list_display = ['name', 'category', 'brand', 'details', 'formatted_price', 'stock', 'photos']
    list_filter = ['category', 'brand', 'is_active']
    search_fields = ['name', 'category', 'brand', 'price', 'stock', 'is_active']
    ordering = ['name', 'category', 'brand', 'price', 'stock']
    actions = [disable_selected, enable_selected]


    def photos(self, obj):
        products = ProductPhoto.objects.filter(product=obj)
        html = render_to_string('admin/product_carousel.html', {'products': products})
        return format_html(html)


    def details(self, obj):
        html = render_to_string('admin/product_description.html', {'description': obj.description})
        return format_html(html)


    photos.short_description = 'Fotografías'
    details.short_description = 'Descripción'