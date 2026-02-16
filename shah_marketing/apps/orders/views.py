from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.accounts.permissions import IsAdminRole
from apps.products.models import Product

from .models import Cart, CartItem, Order
from .serializers import (
    CartItemCreateSerializer,
    CartSerializer,
    CreateOrderSerializer,
    OrderSerializer,
)


class CartAddView(APIView):
    def post(self, request):
        serializer = CartItemCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        product = Product.objects.get(id=serializer.validated_data['product_id'], is_active=True)
        quantity = serializer.validated_data['quantity']

        cart, _ = Cart.objects.get_or_create(user=request.user)
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={'quantity': quantity},
        )

        if not created:
            cart_item.quantity += quantity
            cart_item.save(update_fields=['quantity'])

        return Response({'detail': 'Item added to cart.'}, status=status.HTTP_201_CREATED)


class CartView(generics.RetrieveAPIView):
    serializer_class = CartSerializer

    def get_object(self):
        cart, _ = Cart.objects.get_or_create(user=self.request.user)
        return cart


class CartRemoveView(APIView):
    def delete(self, request, pk):
        cart, _ = Cart.objects.get_or_create(user=request.user)
        deleted, _ = cart.items.filter(id=pk).delete()
        if not deleted:
            return Response({'detail': 'Item not found in cart.'}, status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_204_NO_CONTENT)


class CreateOrderView(generics.CreateAPIView):
    serializer_class = CreateOrderSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order = serializer.save()
        output = OrderSerializer(order)
        return Response(output.data, status=status.HTTP_201_CREATED)


class OrderListView(generics.ListAPIView):
    serializer_class = OrderSerializer

    def get_queryset(self):
        if self.request.user.role == 'ADMIN':
            return Order.objects.select_related('user').prefetch_related('items__product')
        return Order.objects.filter(user=self.request.user).prefetch_related('items__product')


class OrderDetailView(generics.RetrieveAPIView):
    serializer_class = OrderSerializer
    lookup_field = 'id'

    def get_queryset(self):
        queryset = Order.objects.prefetch_related('items__product')
        if self.request.user.role == 'ADMIN':
            return queryset
        return queryset.filter(user=self.request.user)


class AdminOrderStatusUpdateView(generics.UpdateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAdminRole]

    def patch(self, request, *args, **kwargs):
        order = self.get_object()
        status_value = request.data.get('status')
        valid_statuses = {choice for choice, _ in Order.Status.choices}

        if status_value not in valid_statuses:
            return Response({'detail': 'Invalid status.'}, status=status.HTTP_400_BAD_REQUEST)

        order.status = status_value
        order.save(update_fields=['status'])
        return Response(OrderSerializer(order).data, status=status.HTTP_200_OK)
