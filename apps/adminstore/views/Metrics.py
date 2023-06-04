from datetime import datetime, timedelta

from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin
from django.db.models import Avg, Count, Sum
from django.db.models.functions import ExtractMonth
from django.shortcuts import redirect, render
from django.views import View

from apps.accounts.models import Contact, User
from apps.shop.models import Brand, Category, Product, PurchaseOrder, Review, ShoppingCartProduct




class Metrics(UserPassesTestMixin, View):
    """
    Muestra las métricas obtenidas a partir de la información de la base de datos.
    """


    def test_func(self):
        """
        Solamente están autorizados a acceder a esta página los
        usuarios con el atributo is_staff=True.
        """
        return self.request.user.is_staff


    def handle_no_permission(self):
        """
        Si un usuario tiene acceso denegado, se redirecciona al inicio.
        """
        messages.warning(self.request, '¡Acceso denegado!')
        return redirect('shop:home')


    def get(self, request):
        """
        Muestra distintos gráficos de métricas para la tienda virtual.
        """
        # Obtenemos el número de usuarios registrados.
        num_users = User.objects.filter(is_active=True).count()

        # Obtenemos el número de órdenes de compra realizadas durante el último mes.
        now = datetime.now()
        previous_month = now - timedelta(days=30)
        num_orders = PurchaseOrder.objects.filter(created_at__gte=previous_month, status='D').count()

        # Obtenemos el número de unidades vendidas durante el último mes.
        num_units = ShoppingCartProduct.objects.filter(cart__purchaseorder__created_at__gte=previous_month).aggregate(total=Sum('amount'))['total']

        # Obtenemos el total de ventas del último mes.
        total_sales = PurchaseOrder.objects.filter(created_at__gte=previous_month, status='D').aggregate(total=Sum('total'))['total']

        # Obtenemos el total de impuestos recaudados del último mes.
        total_taxes = PurchaseOrder.objects.filter(created_at__gte=previous_month, status='D').aggregate(total=Sum('taxes'))['total']

        # Obtenemos los 5 productos más vendidos.
        # total_sales es el total de unidades vendidas por producto.
        top_products = Product.objects.filter(shoppingcartproduct__cart__purchaseorder__status='D').annotate(total_sales=Sum('shoppingcartproduct__amount')).order_by('-total_sales')[:5]
        top_products = [(item.name, item.total_sales) for item in top_products]

        # Obtenemos las 5 categorías más vendidas.
        top_categories = Category.objects.filter(product__shoppingcartproduct__cart__purchaseorder__status='D').annotate(total_sales=Sum('product__shoppingcartproduct__amount')).order_by('-total_sales')[:5]
        top_categories = [(item.name, item.total_sales) for item in top_categories]

        # Obtenemos las 5 marcas más vendidas.
        top_brands = Brand.objects.filter(product__shoppingcartproduct__cart__purchaseorder__status='D').annotate(total_sales=Sum('product__shoppingcartproduct__amount')).order_by('-total_sales')[:5]
        top_brands = [(item.name, item.total_sales) for item in top_brands]

        # Obtenemos el valor promedio de las reseñas.
        average_rating = Review.objects.aggregate(avg_rating=Avg('rating'))['avg_rating']

        # Obtenemos el municipio desde donde más se compra.
        top_cities = Contact.objects.filter(user__orders__status='D').annotate(total=Count('city')).order_by('-total')[:5]
        top_cities = [(item.city.name, item.total) for item in top_cities]

        # Obtener las ganancias por mes del último año.
        year = now.year
        earnings_per_month = PurchaseOrder.objects.filter(created_at__year=year, status='D').annotate(month=ExtractMonth('created_at')).order_by('month').annotate(earnings=Sum('total')).values('month', 'earnings')
        earnings_per_month = [(item['month'], item['earnings']) for item in earnings_per_month]


        context = {
            'now': now,
            'num_users': num_users,
            'num_orders': num_orders,
            'num_units': num_units,
            'total_sales': total_sales,
            'total_taxes': total_taxes,
            'top_products': top_products,
            'top_categories': top_categories,
            'top_brands': top_brands,
            'average_rating': average_rating,
            'top_cities': top_cities,
            'earnings_per_month': earnings_per_month,
        }

        return render(request, 'adminstore/metrics/show.html', context)