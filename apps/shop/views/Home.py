from django.shortcuts import get_object_or_404,render
from django.db.models import Avg, Count, Sum
from django.views import View

from apps.shop.models import Product, ProductDiscount, ShoppingCartProduct


class Home(View):

    def get(self, request):
        
        # User
        user = request.user
        
        # Productos con descuento
        products_discount = ProductDiscount.objects.prefetch_related(
            'product__photos'
            ).select_related(
            'product'
            ).annotate(
            average_rating=Avg('product__reviews__rating'),
            review_count=Count('product__reviews')
            ).filter(
            product__is_active=True
            ).order_by(
            '-product__created_at'
            )[:12]
        
        products = Product.objects.prefetch_related(
            'photos'
            ).annotate(
                average_rating=Avg('reviews__rating'),
                review_count=Count('reviews')
            ).filter(
                is_active=True
            ).exclude(
                discounts__isnull=False
            ).order_by(
            '-created_at'
            )[:12]
        
        # Carrito de compras
        count_cart_products = ShoppingCartProduct.objects.filter(
            cart__user=user,
            cart__is_active=True
        ).aggregate(total_productos=Sum('amount'))


        context = {
            'user': user,
            'count_cart_products' : count_cart_products['total_productos'] or 0,
            'path': request.path,
            'products_discount': products_discount,
            'products' : products,
        }
        return render(request, 'shop/home.html', context)