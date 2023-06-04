from django.views import View
from django.shortcuts import get_object_or_404,render

from apps.shop.models import ShoppingCart

from decimal import Decimal

class Cart(View):

    def get(self, request, cart_id):

        user = request.user

        cart = get_object_or_404(ShoppingCart, pk=cart_id)
        products = cart.shoppingcartproduct_set.all()

        subtotal = sum(product.product.price * product.amount for product in products)

         # Calcula los impuestos según tu lógica de negocios
        impuestos = subtotal * Decimal('0.19')

        # Calcula el total sumando el subtotal y los impuestos
        total = subtotal + impuestos
        context = {
            'user' : user,
            'products' : products,
            'subtotal' : subtotal,
            'impuestos' : impuestos,
            'total' : total
        }
        return render(request, 'shop/cart.html', context)
    
    def post(self):
        pass