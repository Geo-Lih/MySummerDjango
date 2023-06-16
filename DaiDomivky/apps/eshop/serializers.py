from apps.eshop.models import Order, OrderItem, Payment, Product, Shipment

from rest_framework import serializers


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price']


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['product', 'quantity']  # no order

    # getting or creating order
    def create(self, validated_data):
        user = self.context['request'].user
        order, created = Order.objects.get_or_create(user=user, status='Active')
        validated_data['order'] = order  # creating field 'order'
        return super().create(validated_data)


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['order', 'system', 'status']

    def create(self, validated_data):
        order = validated_data['order']
        order.calculate_total_price()
        order.save()

        validated_data['total_price'] = order.total_price

        return super().create(validated_data)


class ShipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shipment
        fields = ['order', 'delivery_company', 'addressee_first_name', 'addressee_last_name', 'addressee_phone']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    payment = PaymentSerializer(many=True, read_only=True)
    shipment = ShipmentSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['user', 'status', 'total_price', 'created_at', 'items', 'payment', 'shipment']
