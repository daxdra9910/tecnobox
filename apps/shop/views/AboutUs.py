from django.shortcuts import render
from django.views import View
from django.db.models import Sum, Max
from apps.shop.models import ShoppingCartProduct, ShoppingCart




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

        if user.is_authenticated:
            # Obtener el carrito del usuario
            try:
                shopping_cart = ShoppingCart.objects.get(user=user, is_active=True)
            except ShoppingCart.DoesNotExist:
                shopping_cart = None
            
            # Obtener la cantidad de productos en el carrito
            if shopping_cart:
                product_count = ShoppingCartProduct.objects.filter(cart=shopping_cart).count()
            else:
                product_count = 0
        else:
            product_count = None

        context = {
            'user' : user,
            'products_cart_count': product_count,
            'path' : request.path
        }
        return render(request, 'shop/about_us.html', context)