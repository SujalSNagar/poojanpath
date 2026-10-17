from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [

    path('checkout/', views.checkout_page, name='checkout' ),
    path('verify-payment/',views.verify_payment,name='verify_payment'),
    path('payment-failed/<uuid:public_order_id>/', views.payment_failed, name='payment_failed'),
    path('success/',views.order_success,name='success'),

    path('my-orders/',views.my_orders,name='my_orders'),
    path('<uuid:public_order_id>/',views.order_detail,name='order_detail'),

    path('track/',views.track_order,name='track_order'),

    path(

    'cancel/<uuid:public_order_id>/',

    views.cancel_order,

    name='cancel_order'
),

]