import locale

from django.db import models
from django.utils.translation import gettext_lazy as _




class Product(models.Model):
    """
    Información de los productos de la tienda.
    """
    category = models.ForeignKey('shop.Category', on_delete=models.CASCADE, verbose_name=_('categoría'))
    brand = models.ForeignKey('shop.Brand', on_delete=models.CASCADE, verbose_name=_('marca'))
    name = models.CharField(max_length=75, verbose_name=_('nombre'))
    description = models.TextField(verbose_name=_('descripción'))
    price = models.DecimalField(max_digits=13, decimal_places=2, verbose_name=_('precio'))
    stock = models.IntegerField(verbose_name=_('cantidad'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('fecha de creación'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('fecha de actualización'))
    is_active = models.BooleanField(default=True, verbose_name=_('activo'))


    @property
    def formatted_price(self):
        """
        Crea un nuevo atributo que corresponde al precio formateado con los separadors
        de mil y antecedido del símbolo dólar.
        """
        locale.setlocale(locale.LC_ALL, '')  # configuración regional del sistema.
        number = locale.format('%d', self.price, grouping=True)
        return f'${number}'


    def __str__(self):
        return f'{self.name}'


    class Meta:
        verbose_name = _('producto')
        verbose_name_plural = _('productos')