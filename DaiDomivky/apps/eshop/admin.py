from django.contrib import admin

from .models import Order, OrderItem, Payment, Product, Shipment


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'description']


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'product', 'quantity']


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['system', 'status', 'order', 'total_price']


@admin.register(Shipment)
class ShipmentAdmin(admin.ModelAdmin):
    list_display = ['order', 'delivery_company', 'addressee_first_name', 'addressee_last_name', 'addressee_phone']


@admin.register(Order)
class PurchaseHistoryAdmin(admin.ModelAdmin):
    list_display = ['user', 'status', 'total_price', 'created_at']
