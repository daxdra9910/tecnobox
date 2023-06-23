from io import BytesIO
from decimal import Decimal

from django.http import HttpResponse
from django.template.loader import get_template
from django.views import View
from django.shortcuts import get_object_or_404,render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.db import transaction

from apps.shop.models import ShoppingCart, ShoppingCartProduct, Product, PurchaseOrder, OrderProduct, PaymentMethod
from apps.accounts.models import Contact

from xhtml2pdf import pisa



def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None



class Cart(LoginRequiredMixin,View):

    login_url = reverse_lazy('accounts:signin')

    def get(self, request):

        # Obtener el usuario autenticado
        user = request.user

        # Obtener el carrito del usuario
        try:
            shopping_cart = ShoppingCart.objects.get(user=user, is_active=True)
        except ShoppingCart.DoesNotExist:
            shopping_cart = None

        # Obtener los productos en el carrito y calcular el total del valor de la compra
        products = []
        total_price = 0
        total_discount = 0
        if shopping_cart:
            cart_products = ShoppingCartProduct.objects.filter(cart=shopping_cart)
            product_instances = {}
            for cart_product in cart_products:
                product = cart_product.product
                if product in product_instances:
                    product_instances[product] += cart_product.amount
                else:
                    product_instances[product] = cart_product.amount
                total_price += product.price * cart_product.amount

            # Crear una lista de productos únicos con la cantidad de unidades, precio con descuento y subtotal
            for product, amount in product_instances.items():
                discount_price = product.price
                if product.discounts.exists():
                    discount = product.discounts.first()
                    discount_price -= discount.discount_value
                    total_discount += discount.discount_value*amount
                subtotal = discount_price * amount
                products.append({
                    'product': product,
                    'amount': amount,
                    'subtotal': subtotal,
                    'price_with_discount': discount_price
                })

        context = {
            'products': products,
            'total_price': total_price,
            'total_discount': total_discount,
            'products_cart_count': len(products)
        }
        return render(request, 'shop/cart.html', context)

    def increase_quantity(request, product_id):
        # Obtener el producto seleccionado
        product = Product.objects.get(pk=product_id)

        # Verificar si el carrito de compras ya existe para el usuario actual
        cart, created = ShoppingCart.objects.get_or_create(user=request.user)

        # Verificar si el producto ya está en el carrito de compras
        cart_product, created = ShoppingCartProduct.objects.get_or_create(cart=cart, product=product)

        # Incrementar la cantidad del producto en el carrito
        cart_product.amount += 1
        cart_product.save()

        return redirect('shop:cart')  # Redirigir a la página del carrito de compras


    def decrease_quantity(request, product_id):
        # Obtener el producto seleccionado
        product = Product.objects.get(pk=product_id)

        # Obtener el carrito de compras del usuario actual
        cart = ShoppingCart.objects.get(user=request.user)

        # Obtener el producto en el carrito de compras
        cart_product = ShoppingCartProduct.objects.get(cart=cart, product=product)

        # Disminuir la cantidad del producto en el carrito
        if cart_product.amount > 1:
            cart_product.amount -= 1
            cart_product.save()

        return redirect('shop:cart')  # Redirigir a la página del carrito de compras


    def remove_from_cart(request, product_id):
        # Obtener el producto seleccionado
        product = Product.objects.get(pk=product_id)

        # Obtener el carrito de compras del usuario actual
        cart = ShoppingCart.objects.get(user=request.user)

        # Obtener el producto en el carrito de compras
        cart_product = ShoppingCartProduct.objects.get(cart=cart, product=product)

        # Eliminar el producto del carrito
        cart_product.delete()

        return redirect('shop:cart')  # Redirigir a la página del carrito de compras

    def empty_cart(request):
        # Obtener el carrito de compras del usuario actual
        shopping_cart = ShoppingCart.objects.get(user=request.user)

        # Obtener los productos
        products = ShoppingCartProduct.objects.filter(cart= shopping_cart)

        # Eliminar los productos del carrito
        products.all().delete()
        shopping_cart.delete()

        return redirect('shop:cart')  # Redirigir a la página del carrito de compras

    def purchase(request):
        # User
        user = request.user

        # Obtener el carrito de compras del usuario actual
        cart = ShoppingCart.objects.get(user=user, is_active=True)

        # Crear una nueva orden de compra.
        with transaction.atomic():
            # Calcular los valores de subtotal, impuestos y total
            subtotal = Decimal('0.00')
            taxes = Decimal('0.00')
            total = Decimal('0.00')

            cart_products = ShoppingCartProduct.objects.filter(cart=cart)

            for cart_product in cart_products:
                subtotal += cart_product.product.price * cart_product.amount

            taxes = subtotal * Decimal('0.19')
            total = subtotal + taxes

            # Obtener la dirección del usuario.
            address = Contact.objects.get(user=user)

            # Método de pago predefinido.
            payment_method = PaymentMethod.objects.get(pk=1)

            try:
                order = PurchaseOrder.objects.get(shopping_cart=cart)
            except:
                # Crear la orden de compra
                order = PurchaseOrder.objects.create(
                    user=user,
                    shopping_cart=cart,
                    shipping_address=address,
                    subtotal=subtotal,
                    taxes=taxes,
                    total=total,
                    payment_method=payment_method,
                    status='P'  # Estado inicial: En proceso
                )

            # Obtener los productos del carrito
            cart_products = ShoppingCartProduct.objects.filter(cart=cart)

            # Guardar cada producto del carrito en la tabla OrderProduct
            for cart_product in cart_products:
                OrderProduct.objects.create(
                    product=cart_product.product,
                    order=order,
                    amount=cart_product.amount
                )

            # Vaciar el carrito de compras
            # cart.is_active = False
            # cart.save()
        return redirect('shop:bill')



class FacturaPDF(View):
    def get(self, request, *args, **kwargs):
        # Obtener el usuario autenticado
        user = request.user

        # Obtener el carrito del usuario
        shopping_cart = ShoppingCart.objects.get(user=user, is_active=True)

        # Obtener los productos en el carrito y calcular el total del valor de la compra
        products = []
        total_price = 0
        total_discount = 0
        cart_products = ShoppingCartProduct.objects.filter(cart=shopping_cart)
        product_instances = {}
        for cart_product in cart_products:
            product = cart_product.product
            if product in product_instances:
                product_instances[product] += cart_product.amount
            else:
                product_instances[product] = cart_product.amount
            total_price += product.price * cart_product.amount

        # Crear una lista de productos únicos con la cantidad de unidades, precio con descuento y subtotal
        for product, amount in product_instances.items():
            discount_price = product.price
            if product.discounts.exists():
                discount = product.discounts.first()
                discount_price -= discount.discount_value
                total_discount += discount.discount_value*amount
            subtotal = discount_price * amount
            products.append({
                'product': product,
                'amount': amount,
                'subtotal': subtotal,
                'price_with_discount': discount_price
            })

        order = shopping_cart.purchaseorder

        data = {
            'order': order,
            'products': products,
            'total_price': total_price,
            'total_discount': total_discount,
            'products_cart_count': len(products)
        }
        pdf = render_to_pdf('shop/bills/bill.html', data)
        return HttpResponse(pdf, content_type='application/pdf')