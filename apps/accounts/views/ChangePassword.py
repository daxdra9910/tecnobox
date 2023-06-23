from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import redirect, render
from django.views import View
from apps.shop.models import ShoppingCart, ShoppingCartProduct




class ChangePassword(LoginRequiredMixin, View):
    """
    Cambia la contraseña del usuario autenticado.
    """
    login_url = reverse_lazy('accounts:signin')

    def get(self, request):
        """
        Muestra el formulario para cambiar la contraseña.
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
        return render(request, 'accounts/profile/change_password.html', context)


    def post(self, request):
        """
        Cambia la contraseña del usuario.
        """
        # Obtenemos los datos del formulario.
        password = request.POST['password1']

        # Obtenemos el usuario autenticado.
        user = request.user

        # Validamos que el usuario no cambie la contraseña por la misma.
        if user.check_password(password):
            messages.error(request, 'La contraseña no puede ser la misma!')
            return redirect('accounts:change-password')

        # Actualizamos la contraseña del usuario en la base de datos.
        user.set_password(password)
        user.save()

        # Mostramos un mensaje indicando que el proceso ha sido exitoso.
        messages.success(
            request, 'Tu contraseña ha cambiado. Por favor inicia sesión de nuevo')

        # Redirigimos al usuario a la vista de login para que inicie sesión.
        return redirect('accounts:signin')