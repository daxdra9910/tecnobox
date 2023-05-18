from django.db import models
from django.utils.translation import gettext_lazy as _




class Discount(models.Model):
    """
    Información sobre los descuentos aplicados a los productos.
    """
    name = models.CharField(max_length=100, verbose_name=_('nombre'))
    percentage = models.DecimalField(max_digits=5, decimal_places=2, verbose_name=_('porcentaje'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('fecha de creación'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('fecha de actualización'))
    finish_at = models.DateTimeField(verbose_name=_('fecha de fin'))
    is_active = models.BooleanField(default=True, verbose_name=_('activo'))


    def __str__(self):
        return f'{self.name} ({self.percentage}% off)'


    class Meta:
        verbose_name = _('descuento')
        verbose_name_plural = _('descuentos')