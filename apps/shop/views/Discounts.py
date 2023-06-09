from django.views import View
from django.shortcuts import render
from django.db.models import Max, Sum, Avg, Count, F, FloatField
from django.db.models.functions import Cast
from apps.shop.models import ProductDiscount, Category, Brand, ShoppingCartProduct

class Discounts(View):

    def get(self, request):

        # User
        user = request.user

        # Obtener todos los productos
        products = ProductDiscount.objects.prefetch_related(
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
            )

        # Obtener las categorías y marcas para los filtros
        categories = Category.objects.all()
        brands = Brand.objects.all()

        # Obtener los parámetros de filtro de la URL
        category_id = request.GET.get('category')
        brand_id = request.GET.get('brand')
        min_price = request.GET.get('min_price')
        max_price = request.GET.get('max_price')

        # Aplicar filtros si están presentes en la URL
        if category_id:
            products = products.filter(product__category_id=category_id)
        if brand_id:
            products = products.filter(product__brand_id=brand_id)
        if min_price:
            products = products.annotate(min_price_discounted=Cast(F('product__price') - F('discount_value'), output_field=FloatField()))
            products = products.filter(min_price_discounted__gte=min_price)
        if max_price:
            products = products.annotate(max_price_discounted=Cast(F('product__price') - F('discount_value'), output_field=FloatField()))
            products = products.filter(max_price_discounted__lte=max_price)

        # Carrito de compras
        
        count_cart_products = {}
        if user.is_authenticated:
            count_cart_products = ShoppingCartProduct.objects.filter(
              cart__user=user,
               cart__is_active=True
            ).aggregate(
                total_productos=Sum('amount'),
                cart_id=Max('cart__id')
                )

        context = {
            'products': products,
            'categories': categories,
            'brands': brands,
            'selected_category': int(category_id) if category_id else None,
            'selected_brand': int(brand_id) if brand_id else None,
            'min_price': min_price,
            'max_price': max_price,
            'count_cart_products': count_cart_products.get('total_productos', 0),
            'cart_id': count_cart_products.get('cart_id', None),
            'path': request.path
        }

        return render(request, 'shop/discounts_list.html', context)