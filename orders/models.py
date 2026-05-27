from django.db import models

from accounts.models import User

from products.models import Product

import uuid


STATE_CHOICES = [

    ('AP', 'Andhra Pradesh'),

    ('AR', 'Arunachal Pradesh'),

    ('AS', 'Assam'),

    ('BR', 'Bihar'),

    ('CG', 'Chhattisgarh'),

    ('DL', 'Delhi'),

    ('GA', 'Goa'),

    ('GJ', 'Gujarat'),

    ('HR', 'Haryana'),

    ('HP', 'Himachal Pradesh'),

    ('JH', 'Jharkhand'),

    ('KA', 'Karnataka'),

    ('KL', 'Kerala'),

    ('MP', 'Madhya Pradesh'),

    ('MH', 'Maharashtra'),

    ('MN', 'Manipur'),

    ('ML', 'Meghalaya'),

    ('MZ', 'Mizoram'),

    ('NL', 'Nagaland'),

    ('OD', 'Odisha'),

    ('PB', 'Punjab'),

    ('RJ', 'Rajasthan'),

    ('SK', 'Sikkim'),

    ('TN', 'Tamil Nadu'),

    ('TS', 'Telangana'),

    ('TR', 'Tripura'),

    ('UP', 'Uttar Pradesh'),

    ('UK', 'Uttarakhand'),

    ('WB', 'West Bengal'),
]


class Address(models.Model):

    user = models.ForeignKey(

        User,

        related_name='addresses',

        on_delete=models.CASCADE
    )

    full_name = models.CharField(
        max_length=140
    )

    mobile_number = models.CharField(
        max_length=10
    )

    address = models.TextField()

    city = models.CharField(
        max_length=120
    )

    state = models.CharField(
        max_length=5,
        choices=STATE_CHOICES
    )

    postal_code = models.CharField(
        max_length=10
    )

    is_default = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return f'{self.user} - {self.city}'



class Order(models.Model):

    STATUS_CHOICES = [

        ('pending', 'Pending'),

        ('confirmed', 'Confirmed'),

        ('shipped', 'Shipped'),

        ('delivered', 'Delivered'),

        ('cancelled', 'Cancelled'),
        
        ('failed', 'Failed'),
    ]


    PAYMENT_METHOD_CHOICES = [

        ('cod', 'Cash On Delivery'),

        ('online', 'Online Payment'),
    ]


    PAYMENT_STATUS_CHOICES = [

        ('pending', 'Pending'),

        ('paid', 'Paid'),

        ('failed', 'Failed'),
    ]


    user = models.ForeignKey(
        User,
        related_name='orders',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    public_order_id = models.UUIDField(

        default=uuid.uuid4,

        editable=False,

        unique=True
    )

    full_name = models.CharField(
        max_length=140
    )

    mobile_number = models.CharField(
        max_length=10
    )

    email = models.EmailField()

    address = models.TextField()

    city = models.CharField(
        max_length=120
    )

    state = models.CharField(
        max_length=5,
        choices=STATE_CHOICES
    )

    postal_code = models.CharField(
        max_length=10
    )

    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_METHOD_CHOICES,
        default='cod'
    )

    payment_status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS_CHOICES,
        default='pending'
    )

    order_status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )

    gateway_order_id = models.CharField(
        max_length=200,
        blank=True
    )

    gateway_payment_id = models.CharField(
        max_length=200,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    estimated_delivery_date = models.DateField(
    null=True,
    blank=True
    )

    class Meta:

        ordering = ['-created_at']


    def __str__(self):

        return f'Order #{self.id}'



class OrderItem(models.Model):

    order = models.ForeignKey(
        Order,
        related_name='items',
        on_delete=models.CASCADE
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.SET_NULL,
        null=True
    )

    quantity = models.PositiveIntegerField(
        default=1
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )


    def __str__(self):

        return f'{self.order.id} - {self.product}'