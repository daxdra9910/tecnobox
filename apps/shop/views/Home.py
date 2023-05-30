from django.shortcuts import get_object_or_404,render
from django.views import View

from apps.shop.models import Product


class Home(View):

    def get(self, request):

        products = Product.objects.all()

        context = {
            'user': request.user,
            'path': request.path,
            'products' : products
        }
        return render(request, 'shop/home.html', context)