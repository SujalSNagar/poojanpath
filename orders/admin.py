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

        'customer_orders_count',

        'total_price',

        'payment_method',

        'payment_status',

        'order_status',

        'created_at',
    )

    list_filter = (

        'order_status',

        'payment_status',

        'payment_method',

        'created_at',
    )

    date_hierarchy = 'created_at'

    search_fields = (

        'full_name',

        'mobile_number',

        'email'
    )

    

    inlines = [
        OrderItemInline
    ]


    def customer_orders_count(self, obj):

        return Order.objects.filter(
            mobile_number=obj.mobile_number
        ).count()

    customer_orders_count.short_description = 'Total Orders'




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

