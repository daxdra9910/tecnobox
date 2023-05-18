from django.shortcuts import render
from django.views import View




class TermsAndConditions(View):
    """
    Página "Términos y condiciones de uso".
    """

    def get(self, request):
        """
        Muestra información sobre los términos y condiciones de la empresa.
        """
        return render(request, 'shop/terms_and_conditions.html')