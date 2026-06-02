from django.shortcuts import render,redirect,get_object_or_404

from products.models import Product

from .cart import Cart

from django.contrib import messages

from django.http import JsonResponse
from core.utils import get_delivery_dates

def cart_detail(request):

    cart = Cart(request)
    start_date, end_date = get_delivery_dates()
    return render(request,'cart/detail.html',
        {
            'cart': cart,
            'start_date': start_date,
            'end_date': end_date
        }
    )


def cart_add(request, product_id):

    if request.method == 'POST':

        cart = Cart(request)

        product = get_object_or_404(Product, id=product_id)

        if product.stock <= 0:

            return JsonResponse({
                'success': False,
                'message': 'Product is out of stock.'
            })

        cart.add(product=product)

    return JsonResponse({
        'success': True,
        'message': 'Added to cart',
        'cart_count': len(cart)
    })



def cart_increase(request, product_id):

    cart = Cart(request)

    product = get_object_or_404(
        Product,
        id=product_id
    )

    cart.increase(product)

    return redirect('cart:detail')



def cart_decrease(request, product_id):

    cart = Cart(request)

    product = get_object_or_404(
        Product,
        id=product_id
    )

    cart.decrease(product)

    return redirect('cart:detail')


def cart_remove(request, product_id):

    cart = Cart(request)

    product = get_object_or_404(Product, id=product_id)

    cart.remove(product)

    return redirect('cart:detail')


def cart_clear(request):

    cart = Cart(request)

    cart.clear()

    return redirect('cart:detail')