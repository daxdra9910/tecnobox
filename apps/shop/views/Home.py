from django.shortcuts import render
from django.db.models import Avg, Count
from django.views import View

from apps.shop.models import Product, ProductDiscount, ShoppingCart, ShoppingCartProduct


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
            'products_cart_count': product_count,
            'path': request.path,
            'products_discount': products_discount,
            'products' : products,
        }
        return render(request, 'shop/home.html', context)