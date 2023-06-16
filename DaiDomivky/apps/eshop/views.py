from apps.eshop.models import Order, OrderItem, Payment, Product, Shipment

from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveAPIView, UpdateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import OrderItemSerializer, OrderSerializer, PaymentSerializer, ProductSerializer, ShipmentSerializer


# Create your views here.


class ProductList(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductDetail(RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ActiveOrderDetail(RetrieveAPIView):
    serializer_class = OrderSerializer

    def get_object(self):
        try:
            active_order = Order.objects.get(status='Active')
            return active_order
        except Order.DoesNotExist:
            raise NotFound('No active order found.')


class OrdersHistoryList(ListAPIView):
    serializer_class = OrderSerializer
    queryset = Order.objects.filter(status='Completed')


class OrderItemCreate(ListCreateAPIView):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer

    # providing request to serializer context to have access to user
    def get_serializer_context(self):
        return {'request': self.request}


class PaymentAndShipmentCreate(APIView):

    def post(self, request):
        user = request.user
        active_order = Order.objects.get(user=user, status='Active')

        # Add the active order to the request data
        request.data['order'] = active_order.id
        # Providing new request.data to serializers
        payment_serializer = PaymentSerializer(data=request.data)
        shipment_serializer = ShipmentSerializer(data=request.data)
        # payment_serializer.is_valid() -> bool
        #                   .save()     -> obj
        #                   .data       -> json

        if payment_serializer.is_valid() and shipment_serializer.is_valid():
            payment_serializer.save()
            shipment_serializer.save()

            return Response({
                'payment': payment_serializer.data,
                'shipment': shipment_serializer.data
            }, status=status.HTTP_201_CREATED)

        return Response({
            'payment': payment_serializer.errors,
            'shipment': shipment_serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class PaymentUpdate(UpdateAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    def perform_update(self, serializer):  # serializer = PaymentSerializer()
        instance = serializer.save()  # saving updated payment obj

        # If the payment is completed, mark the related order as completed as well
        if instance.status == 'Completed':
            order = instance.order
            order.status = 'Completed'
            order.save()

        return super().perform_update(serializer)


class ShipmentUpdate(UpdateAPIView):
    queryset = Shipment.objects.all()
    serializer_class = ShipmentSerializer
