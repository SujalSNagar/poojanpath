from django.shortcuts import render,redirect,get_object_or_404

from products.models import Product

from .cart import Cart


def cart_detail(request):

    cart = Cart(request)

    return render(request,'cart/detail.html',
        {
            'cart': cart
        }
    )


def cart_add(request, product_id):

    if request.method == 'POST':

        cart = Cart(request)

        product = get_object_or_404(Product, id=product_id)

        cart.add(product=product)

    return redirect('cart:detail')


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