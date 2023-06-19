from apps.user.models import CustomUser

from django.db import models


# Create your models here.


class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(max_length=20000)
    price = models.DecimalField(max_digits=6, decimal_places=2)


ACTIVE = 'Active'
COMPLETED = 'Completed'
PROCESSING = 'Processing'
CANCELED = 'Canceled'
STATUS_CHOICE = [
    (ACTIVE, 'Active'),
    (PROCESSING, 'Processing'),
    (COMPLETED, 'Completed'),
    (CANCELED, 'Canceled'),
]


class Order(models.Model):
    status = models.CharField(max_length=15, choices=STATUS_CHOICE, default=ACTIVE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'status'], condition=models.Q(status=ACTIVE),
                                    name='unique_active_order'),
        ]

    def calculate_total_price(self):
        order_items = self.items.all()
        self.total_price = sum(item.product.price * item.quantity for item in order_items)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.PROTECT, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'{self.order} {self.product} {self.quantity}'


class Payment(models.Model):
    PAYPAL = 'PayPal'
    LIQPAY = 'Liqpay'
    PORTMONE = 'Portmone'
    PAYMENT_SYSTEM_CHOICE = [
        (PAYPAL, 'PayPal'),
        (LIQPAY, 'Liqpay'),
        (PORTMONE, 'Portmone'),
    ]
    order = models.ForeignKey(Order, on_delete=models.PROTECT, related_name='payment')
    system = models.CharField(max_length=30, choices=PAYMENT_SYSTEM_CHOICE, default=PAYPAL)
    status = models.CharField(max_length=15, choices=STATUS_CHOICE, default=PROCESSING)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)


class Shipment(models.Model):
    NEWPOST = 'NP'
    UKRPOST = 'UkrP'
    MEEST = 'MT'
    JUSTIN = 'JN'
    DELIVERY_COMPANY = [
        (NEWPOST, 'New Post'),
        (UKRPOST, 'Ukr Post'),
        (MEEST, 'Meest'),
        (JUSTIN, 'Justin'),
    ]
    order = models.ForeignKey(Order, on_delete=models.PROTECT, related_name='shipment')
    delivery_company = models.CharField(max_length=10, choices=DELIVERY_COMPANY, default='')
    addressee_first_name = models.CharField(max_length=32)
    addressee_last_name = models.CharField(max_length=32)
    addressee_phone = models.CharField(max_length=10)
