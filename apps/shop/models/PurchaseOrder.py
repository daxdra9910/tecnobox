from decimal import Decimal

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
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='orders', verbose_name=_('cliente'))
    shopping_cart = models.OneToOneField('shop.ShoppingCart', on_delete=models.CASCADE, verbose_name=_('carrito de compras'))
    shipping_address = models.ForeignKey('accounts.Contact', on_delete=models.CASCADE, verbose_name=_('dirección de entrega'))
    subtotal = models.DecimalField(max_digits=13, decimal_places=2, verbose_name=_('subtotal'))
    taxes = models.DecimalField(max_digits=13, decimal_places=2, verbose_name=_('impuestos'))
    total = models.DecimalField(max_digits=13, decimal_places=2, verbose_name=_('total'))
    payment_method = models.ForeignKey('shop.PaymentMethod', on_delete=models.CASCADE, verbose_name=_('método de pago'))
    status =  models.CharField(max_length=1, choices=STATUS_CHOICES, default='P', verbose_name=_('estado'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('fecha de creación'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('fecha de actualización'))
    is_active = models.BooleanField(default=True, verbose_name=_('activo'))


    def save(self, *args, **kwargs):
        """
        Sobrescribimos el método save() para calcular el valor de subtotal, taxes y total
        antes de guardar el registro en la base de datos.
        """
        # Calculamos el subtotal.
        subtotal = Decimal('0.00')
        cart_products = self.shopping_cart.shoppingcartproduct_set.all()

        for cart_product in cart_products:
            subtotal += cart_product.product.price * cart_product.amount

        self.subtotal = subtotal

        # calculamos los impuestos (IVA del 19%).
        impuesto = Decimal('0.19')
        self.taxes = subtotal * impuesto

        # Calculos el total.
        self.total = self.subtotal + self.taxes

        # Guardamos la instancia.
        super().save(*args, **kwargs)


    def __str__(self):
        return f'Order #{self.pk} de {self.user.username}'


    class Meta:
        verbose_name = _('orden de compra')
        verbose_name_plural = _('órdenes de compra')