from django.shortcuts import render
from django.views import View
from django.db.models import Sum, Max
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
        count_cart_products = {}
        if user.is_authenticated:
            count_cart_products = ShoppingCartProduct.objects.filter(
              cart__user=user,
               cart__is_active=True
            ).aggregate(
                total_productos=Sum('amount'),
                cart_id=Max('cart_id')
                )

        context = {
            'user' : user,
            'count_cart_products' : count_cart_products.get('total_productos', 0),
            'cart_id' : count_cart_products.get('cart_id', 0),
            'path' : request.path
        }
        return render(request, 'shop/about_us.html', context)