from django.db import models
from django.utils.translation import gettext_lazy as _




class ShoppingCartProduct(models.Model):
    """
    Relación muchos a muchos entre los productos y los carritos de compra.
    """
    product = models.ForeignKey('shop.Product', on_delete=models.CASCADE, verbose_name=_('producto'))
    cart = models.ForeignKey('shop.ShoppingCart', on_delete=models.CASCADE, verbose_name=_('carrito de compras'))
    amount = models.IntegerField(verbose_name=_('cantidad'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('fecha de creación'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('fecha de actualización'))
    is_active = models.BooleanField(default=True, verbose_name=_('activo'))


    def __str__(self):
        return f'{self.product.name} of {self.cart.user.username} cart'


    class Meta:
        verbose_name = _('productos del carrito de compras')
        verbose_name_plural = _('productos del carrito de compras')