from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View

from apps.accounts.models import City




class Metrics(LoginRequiredMixin, View):
    """
    Tablero con las métricas más importantes de la tienda.
    """
    login_url = reverse_lazy('accounts:signin')

    def get(self, request):
        """
        Muestra un conjunto de gráficos.
        """
        return render(request, 'admin/metrics.html')




class CitiesByRegion(View):
    """
    Muestra un objeto JSON con las ciudades de un departamento dado.
    Esto con el fin de servir datos que sean consumibles por JavaScript.
    """

    def get(self, request, region_id):
        cities = City.objects.filter(region=region_id, is_active=True)
        data = []

        for city in cities:
            item = {
                'id': city.id,
                'name': city.name,
            }
            data.append(item)

        # Como los datos no son un diccionario, se usa safe=False.
        return JsonResponse(data, safe=False)