from django.shortcuts import render
from django.views import View
from django.db.models import Sum
from apps.shop.models import ShoppingCartProduct




class AboutUs(View):
    """
    Página "Sobre Nosotros".
    """

    def get(self, request):
        """
        Muestra la página con información sobre la empresa.
        """

        # User
        user = request.user

        # Carrito de compras
        count_cart_products = ShoppingCartProduct.objects.filter(
            cart__user=user,
            cart__is_active=True
        ).aggregate(total_productos=Sum('amount'))

        context = {
            'user' : user,
            'count_cart_products' : count_cart_products['total_productos'] or 0,
            'path' : request.path
        }
        return render(request, 'shop/about_us.html', context)