from django.shortcuts import render
from django.views import View
from apps.shop.models import ShoppingCartProduct, ShoppingCart



class TermsAndConditions(View):
    """
    Página "Términos y condiciones de uso".
    """

    def get(self, request):
        """
        Muestra información sobre los términos y condiciones de la empresa.
        """

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
            'user': user,
            'products_cart_count': product_count
        }

        return render(request, 'shop/terms_and_conditions.html', context)