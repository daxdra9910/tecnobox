from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import redirect, render
from django.views import View
from apps.shop.models import ShoppingCartProduct, ShoppingCart




class ContactUs(View):
    """
    Página "Contáctenos".
    """

    def get(self, request):
        """
        Muestra el formulario de contacto.
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
        return render(request, 'shop/contact_us.html', context)


    def post(self, request):
        """
        Envia un mensaje del usuario al correo de la empresa.
        (la dirección de correo está definida en config/.env).
        """
        # Obtenemos los datos del formulario.
        full_name = request.POST['full_name']
        phone = request.POST.get('phone', 'No proporcionado')
        email = request.POST['email']
        message = request.POST['message']

        # Enviamos el email.
        from_email = settings.EMAIL_HOST_USER
        to_list = [settings.EMAIL_HOST_USER]
        subject = 'Mensaje enviado desde el sitio web'
        message = f'Nombre: {full_name}\nEmail: {email}\nTeléfono: {phone}\nMensaje: {message}'

        send_mail(subject, message, from_email, to_list, fail_silently=False)

        # Redirigimos al usuario de nuevo a la vista de contacto.
        messages.success(request, '¡Tu mensaje ha sido enviado!')
        return redirect('shop:contact-us')