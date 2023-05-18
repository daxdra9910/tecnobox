from django.db import models
from django.utils.translation import gettext_lazy as _




class PaymentMethod(models.Model):
    """
    Información sobre los métodos de pago.
    """
    name = models.CharField(max_length=50, verbose_name=_('nombre'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('fecha de creación'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('fecha de actualización'))
    is_active = models.BooleanField(default=True, verbose_name=_('activo'))


    def __str__(self):
        return f'{self.name}'


    class Meta:
        verbose_name = _('método de pago')
        verbose_name_plural = _('métodos de pago')