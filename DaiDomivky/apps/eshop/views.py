from apps.eshop.models import ACTIVE, CANCELED, COMPLETED, Order, OrderItem, PROCESSING, Payment, Product, Shipment

from django.db.models import Q
from django.http import HttpResponseForbidden

from rest_framework import pagination, status
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .permissions import IsOrderCanceled
from .serializers import OrderItemSerializer, OrderSerializer, PaymentSerializer, ProductSerializer, ShipmentSerializer


# Create your views here.


class ProductList(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = pagination.LimitOffsetPagination


class ProductDetail(RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class OrderDetail(RetrieveAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        print(self.kwargs)
        return get_object_or_404(Order, user=self.request.user, pk=self.kwargs.get('pk'))


class OrdersHistoryList(ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = pagination.LimitOffsetPagination

    def get_queryset(self):
        return Order.objects.filter(Q(status=COMPLETED) | Q(status=CANCELED), user=self.request.user)


class OrderItemCreate(CreateAPIView):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    permission_classes = [IsAuthenticated]

    # providing request to serializer context to have access to user
    def get_serializer_context(self):
        return {'request': self.request}


class PaymentAndShipmentCreate(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        if not Order.objects.filter(user=user, status=ACTIVE).exists():
            return HttpResponseForbidden("No active order available for this user.")

        active_order = Order.objects.get(user=user, status=ACTIVE)

        active_order.status = 'Processing'
        active_order.save()

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
    permission_classes = [IsAuthenticated, IsOrderCanceled]

    def perform_update(self, serializer):  # serializer = PaymentSerializer()
        instance = serializer.save()  # saving updated payment obj

        # If the payment is completed, mark the related order as completed as well

        order = instance.order
        order.status = instance.status
        order.save()

        return super().perform_update(serializer)


class ShipmentUpdate(UpdateAPIView):
    queryset = Shipment.objects.all()
    serializer_class = ShipmentSerializer
    permission_classes = [IsAuthenticated, IsOrderCanceled]
