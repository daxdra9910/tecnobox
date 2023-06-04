from django.contrib import admin
from django.template.loader import render_to_string
from django.utils.html import format_html

from apps.utils.actions import BaseModelAdmin, disable_selected, enable_selected
from apps.shop.models import Product, ProductDiscount, ProductPhoto




class ProductPhotoInline(admin.TabularInline):
    """
    Permite añadir fotos en el formulario
    de creación/edición del modelo Product.
    """
    model = ProductPhoto
    readonly_fields = ['image_preview']
    extra = 0




class ProductDiscountInline(admin.TabularInline):
    """
    Permite añadir descuentos en el formulario
    de creación/edición del modelo Product.
    """
    model = ProductDiscount
    fields = ['discount', 'value', 'is_active']
    readonly_fields = ['value']
    extra = 0


    def value(self, obj):
        return obj.formatted_value


    value.short_description = 'Valor'



@admin.register(Product)
class ProductAdmin(BaseModelAdmin):
    """
    Modelo Product de la interfaz de administración.
    """
    inlines = [ProductDiscountInline, ProductPhotoInline]

    list_display = ['title', 'description', 'formatted_price', 'stock']
    list_filter = ['category', 'brand', 'is_active']
    search_fields = ['name', 'category', 'brand', 'price', 'stock', 'is_active']
    ordering = ['name', 'category', 'brand', 'price', 'stock']
    actions = [disable_selected, enable_selected]


    def title(self, obj):
        return format_html(f'{obj.category} ({obj.brand})<br><br>{obj.name}')


    title.short_description = 'Nombre'