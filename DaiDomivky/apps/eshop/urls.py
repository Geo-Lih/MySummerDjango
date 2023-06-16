from django.urls import path

from .views import ActiveOrderDetail, OrderItemCreate, OrdersHistoryList, PaymentAndShipmentCreate, PaymentUpdate, \
    ProductDetail, ProductList, ShipmentUpdate

app_name = 'eshop'

urlpatterns = [
    path('', ProductList.as_view(), name='product_list'),
    path('<int:pk>/', ProductDetail.as_view(), name='product_detail'),
    path('orderitem_create/', OrderItemCreate.as_view(), name='order_item_create'),
    path('order_active/', ActiveOrderDetail.as_view(), name='order_active'),
    path('order_history/', OrdersHistoryList.as_view(), name='order_history'),
    path('payment_update/<int:pk>/', PaymentUpdate.as_view(), name='payment_update'),
    path('shipment_update/<int:pk>/', ShipmentUpdate.as_view(), name='shipment_update'),
    path('checkout_create/', PaymentAndShipmentCreate.as_view(), name='checkout_create'),
]
