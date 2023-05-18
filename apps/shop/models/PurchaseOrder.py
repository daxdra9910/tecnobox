from django.db import models
from django.utils.translation import gettext_lazy as _




class PurchaseOrder(models.Model):
    """
    Información de las órdenes de compra.
    """
    STATUS_CHOICES = (
        ('P', 'En proceso'),
        ('S', 'Enviada'),
        ('D', 'Entregada'),
        ('C', 'Cancelada')
    )
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE, verbose_name=_('cliente'))
    subtotal = models.DecimalField(max_digits=13, decimal_places=2, verbose_name=_('subtotal'))
    taxes = models.DecimalField(max_digits=13, decimal_places=2, verbose_name=_('impuestos'))
    total = models.DecimalField(max_digits=13, decimal_places=2, verbose_name=_('total'))
    payment_method = models.ForeignKey('shop.PaymentMethod', on_delete=models.CASCADE, verbose_name=_('método de pago'))
    shipping_address = models.TextField(verbose_name=_('dirección de entrega'))
    status =  models.CharField(max_length=1, choices=STATUS_CHOICES, default='P', verbose_name=_('estado'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('fecha de creación'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('fecha de actualización'))
    is_active = models.BooleanField(default=True, verbose_name=_('activo'))


    def __str__(self):
        return f'Order #{self.pk} de {self.user.username}'


    class Meta:
        verbose_name = _('orden de compra')
        verbose_name_plural = _('órdenes de compra')