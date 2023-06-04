import locale

from django.db import models
from django.utils.translation import gettext_lazy as _




class ProductDiscount(models.Model):
    """
    Relación muchos a muchos entre los productos y sus descuentos.
    """
    product = models.ForeignKey('shop.Product', on_delete=models.CASCADE, related_name='discounts', verbose_name=_('producto'))
    discount = models.ForeignKey('shop.Discount', on_delete=models.CASCADE, verbose_name=_('descuento'))
    discount_value = models.DecimalField(max_digits=13, decimal_places=2, verbose_name=_('valor del descuento'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('fecha de creación'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('fecha de actualización'))
    is_active = models.BooleanField(default=True, verbose_name=_('activo'))


    @property
    def formatted_value(self):
        """
        Crea un nuevo atributo que corresponde al precio formateado con los separadors
        de mil y antecedido del símbolo dólar.
        """
        if self.discount_value:
            locale.setlocale(locale.LC_ALL, '')  # configuración regional del sistema.
            number = locale.format('%d', self.discount_value, grouping=True)
            return f'${number}'
        return '---'


    def save(self, *args, **kwargs):
        # Calculamos el valor del descuento.
        self.discount_value = float(self.product.price) * float(self.discount.percentage) / 100
        super().save(*args, **kwargs)


    def __str__(self):
        return f'{self.product.name} ({self.discount.percentage}% off)'


    class Meta:
        verbose_name = _('producto con descuento')
        verbose_name_plural = _('productos con descuentos')