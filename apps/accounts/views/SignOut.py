from django.contrib import messages
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.views import View




class SignOut(View):
    """
    Cierre de sesión de usuario actual.
    """

    def get(self, request):
        logout(request)
        messages.success(request, '¡Cierre de sesión exitoso!')
        return redirect('shop:home')