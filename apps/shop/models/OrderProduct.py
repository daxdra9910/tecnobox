from django.db import models
from django.utils.translation import gettext_lazy as _




class OrderProduct(models.Model):
    """
    Relación muchos a muchos entre las órdenes de compra y sus productos.
    """
    product = models.ForeignKey('shop.Product', on_delete=models.CASCADE, verbose_name=_('producto'))
    order = models.ForeignKey('shop.PurchaseOrder', on_delete=models.CASCADE, verbose_name=_('orden de compra'))
    amount = models.IntegerField(verbose_name=_('cantidad'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('fecha de creación'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('fecha de actualización'))
    is_active = models.BooleanField(default=True, verbose_name=_('activo'))


    def __str__(self):
        return f'{self.product.name} ({self.discount.percentage}% off)'


    class Meta:
        verbose_name = _('producto de órden de compra')
        verbose_name_plural = _('productos de órdenes de compra')