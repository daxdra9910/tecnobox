from django.db import models
from django.utils.translation import gettext_lazy as _




class ShoppingCart(models.Model):
    """
    Información sobre los carritos de compras.
    """
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE, verbose_name=_('cliente'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('fecha de creación'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('fecha de actualización'))
    is_active = models.BooleanField(default=True, verbose_name=_('activo'))


    def __str__(self):
        return f'Shopping cart of {self.user.username} - #{self.purchase_order.pk}'


    class Meta:
        verbose_name = _('carrito de compra')
        verbose_name_plural = _('carritos de compra')