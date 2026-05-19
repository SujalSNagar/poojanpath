from django.shortcuts import (
    render,
    redirect,
    get_object_or_404
)

from django.contrib.auth.decorators import login_required

from django.contrib import messages

from datetime import timedelta

from django.utils import timezone

from cart.cart import Cart

from .forms import CheckoutForm

from .models import (
    Order,
    OrderItem,
    Address
)

import razorpay

from django.conf import settings

def checkout_page(request):

    cart = Cart(request)

    if len(cart) == 0:

        return redirect('cart:detail')

    saved_addresses = []

    if request.user.is_authenticated:

        saved_addresses = Address.objects.filter(
            user=request.user
        )

    if request.method == 'POST':

        form = CheckoutForm(request.POST)

        if form.is_valid():

            order = form.save(
                commit=False
            )

            order.total_price = (
                cart.get_total_price()
            )

            estimated_delivery_date = (

                timezone.now().date()

                + timedelta(days=5)
            )

            order.estimated_delivery_date = (
                estimated_delivery_date
            )

            if request.user.is_authenticated:

                order.user = request.user

            order.save()

            # CREATE ORDER ITEMS

            for item in cart:

                OrderItem.objects.create(

                    order=order,

                    product=item['product'],

                    quantity=item['quantity'],

                    price=item['price'],

                    total_price=item['total_price']
                )

                # UPDATE STOCK

                product = item['product']

                product.stock -= item['quantity']

                if product.stock <= 0:

                    product.stock = 0

                    product.is_available = False

                product.save()

            # SAVE ADDRESS

            if request.user.is_authenticated:

                address_exists = Address.objects.filter(

                    user=request.user,

                    address=order.address,

                    city=order.city,

                    postal_code=order.postal_code

                ).exists()

                if not address_exists:

                    Address.objects.create(

                        user=request.user,

                        full_name=order.full_name,

                        mobile_number=order.mobile_number,

                        address=order.address,

                        city=order.city,

                        state=order.state,

                        postal_code=order.postal_code
                    )

            # ONLINE PAYMENT

            if order.payment_method == 'online':

                client = razorpay.Client(

                    auth=(

                        settings.RAZORPAY_KEY_ID,

                        settings.RAZORPAY_KEY_SECRET
                    )
                )
                payment = client.order.create({

                    'amount': int(
                        order.total_price * 100
                    ),

                    'currency': 'INR',

                    'payment_capture': 1
                })

                order.gateway_order_id = (
                    payment['id']
                )

                order.save()

                context = {

                    'payment': payment,

                    'order': order,

                    'razorpay_key': (

                        settings.RAZORPAY_KEY_ID
                    )
                }

                return render(

                    request,

                    'orders/payment.html',

                    context
                )

            # COD FLOW

            if order.payment_method == 'cod':

                order.order_status = 'confirmed'

                order.save()

                cart.clear()

                request.session[
                    'last_delivery_date'
                ] = str(
                    estimated_delivery_date
                )

                return redirect(
                    'orders:success'
                )

    else:

        form = CheckoutForm()

    estimated_delivery_date = (

        timezone.now().date()

        + timedelta(days=5)
    )

    context = {

        'cart': cart,

        'form': form,

        'saved_addresses': saved_addresses,

        'estimated_delivery_date':
        estimated_delivery_date,
    }

    return render(

        request,

        'orders/checkout.html',

        context
    )

def verify_payment(request):

    payment_id = request.GET.get(
        'payment_id'
    )

    order_id = request.GET.get(
        'order_id'
    )

    signature = request.GET.get(
        'signature'
    )

    order = get_object_or_404(

        Order,

        gateway_order_id=order_id
    )

    client = razorpay.Client(

        auth=(

            settings.RAZORPAY_KEY_ID,

            settings.RAZORPAY_KEY_SECRET
        )
    )

    try:

        client.utility.verify_payment_signature({

            'razorpay_order_id': order_id,

            'razorpay_payment_id': payment_id,

            'razorpay_signature': signature
        })

        order.payment_status = 'paid'

        order.order_status = 'confirmed'

        order.gateway_payment_id = (
            payment_id
        )

        order.save()

        cart = Cart(request)

        cart.clear()

        request.session[
            'last_delivery_date'
        ] = str(
            order.estimated_delivery_date
        )

        return redirect(
            'orders:success'
        )

    except:

        order.payment_status = 'failed'

        order.order_status = 'failed'

        order.save()

        messages.error(

        request,

        'Payment verification failed.'
        )   

        return redirect(
            'orders:checkout'
        )

def payment_failed(request, order_id):

    order = get_object_or_404(

        Order,

        id=order_id
    )

    order.payment_status = 'failed'

    order.order_status = 'failed'

    order.save()

    messages.error(

    request,

    'Payment failed or cancelled.'
    )

    return redirect(
        'orders:checkout'
    )


def order_success(request):

    estimated_delivery_date = request.session.get(
        'last_delivery_date'
    )

    return render(

        request,

        'orders/order_success.html',

        {

            'estimated_delivery_date':
            estimated_delivery_date
        }
    )

@login_required

def my_orders(request):

    orders = (

        Order.objects

        .filter(user=request.user)

        .prefetch_related(
            'items',
            'items__product'
        )
    )

    return render(

        request,

        'orders/my_orders.html',

        {

            'orders': orders
        }
    )


@login_required

def order_detail(request, order_id):

    order = get_object_or_404(

        Order.objects.prefetch_related(

            'items',

            'items__product'
        ),

        id=order_id,

        user=request.user
    )

    return render(

        request,

        'orders/order_detail.html',

        {

            'order': order
        }
    )


def track_order(request):

    orders = None

    error = None

    if request.method == 'POST':

        mobile_number = request.POST.get(
            'mobile_number'
        )

        orders = Order.objects.filter(

            mobile_number=mobile_number

        ).prefetch_related(

            'items',

            'items__product'
        )

        if not orders.exists():

            error = 'No orders found.'

    return render(

        request,

        'orders/track_order.html',

        {

            'orders': orders,

            'error': error
        }
    )