from django.conf import settings
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.utils import timezone
from django.views import View
from apps.shop.models import ShoppingCart, ShoppingCartProduct

from apps.accounts.models import User




class AskResetPassword(View):
    """
    Muestra un formulario para que el usuario ingrese el correo electrónico a
    donde recibirá un enlace para restablecer la contraseña.
    """

    def get(self, request):
        """
        Muestra el formulario para recibir un correo de restablecimiento de contraseña.
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
        return render(request, 'accounts/reset_password/reset.html', context)


    def post(self, request):
        """
        Envía un correo electrónico con un enlace para restablecer la contraseña.
        """
        # Obtenemos el email del formulario.
        email = request.POST['email']

        try:
            # Buscamos el usuario en la base de datos.
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            # Si el usuario no existe recargamos la página y mostramos un mensaje de advertencia.
            messages.error(request, 'El correo electrónico no está registrado en nuestro sistema.')
            return redirect('accounts:reset-password')

        # Generamos un token único para el usuario.
        token = user.generate_password_reset_token()

        # Enviamos un correo electrónico con el enlace.
        current_site = get_current_site(request)

        from_email = f'TecnoBox <{settings.EMAIL_HOST_USER}>'
        to_list = [user.email]

        subject = 'Instrucciones para restablecer tu contraseña'
        message = render_to_string('accounts/reset_password/email.html', {
            'full_name': user.get_full_name(),
            'domain': current_site.domain,
            'token': token,
        })

        send_mail(subject, message, from_email, to_list, fail_silently=False)

        return render(request, 'accounts/reset_password/reset_done.html')




class ResetPassword(View):
    """
    Muestra un formulario donde el usuario puede restablecer su contraseña.
    """

    def get(self, request, token):
        """
        Muestra el formulario para restablecer la contraseña.
        """
        try:
            # Buscamos el usuario que tenga el token.
            user = User.objects.get(password_reset_token=token)

        except User.DoesNotExist:
            # Si el token no es válido, redirigimos a la página de inicio.
            return redirect('shop:home')

        # Si el token ha expirado, redirigimos a la página de inicio.
        if user.password_reset_token_created_at < (timezone.now() - timezone.timedelta(hours=1)):
            return redirect('shop:home')

        return render(request, 'accounts/reset_password/reset_confirm.html', {'token': token})


    def post(self, request, token):
        # Obtenemos los datos del formulario.
        password = request.POST['password1']

        # Obtenemos el usuario autenticado.
        user = User.objects.get(password_reset_token=token)

        # Actualizamos la contraseña y removemos el token.
        user.set_password(password)
        user.password_reset_token = None
        user.password_reset_token_created_at = None
        user.save()

        # Redirigimos al usuario a una página que indica que el proceso ha sido exitoso.
        return render(request, 'accounts/reset_password/reset_complete.html')