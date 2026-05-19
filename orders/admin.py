from django.contrib import admin

from .models import (
    Order,
    OrderItem,
    Address
)


class OrderItemInline(admin.TabularInline):

    model = OrderItem

    extra = 0


@admin.register(Order)

class OrderAdmin(admin.ModelAdmin):

    list_display = (

        'id',

        'full_name',

        'mobile_number',

        'total_price',

        'payment_method',

        'payment_status',

        'order_status',

        'created_at'
    )

    list_filter = (

        'order_status',

        'payment_status',

        'payment_method'
    )

    search_fields = (

        'full_name',

        'mobile_number',

        'email'
    )

    inlines = [
        OrderItemInline
    ]


@admin.register(Address)

class AddressAdmin(admin.ModelAdmin):

    list_display = (

        'id',

        'user',

        'full_name',

        'city',

        'state',

        'postal_code',

        'is_default'
    )

    search_fields = (

        'full_name',

        'mobile_number',

        'city'
    )