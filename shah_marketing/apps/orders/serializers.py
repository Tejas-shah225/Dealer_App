from decimal import Decimal

from django.db import transaction
from rest_framework import serializers

from apps.products.models import Product
from apps.products.serializers import ProductSerializer

from .models import Cart, CartItem, Order, OrderItem


class CartItemCreateSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1)

    def validate_product_id(self, value):
        if not Product.objects.filter(id=value, is_active=True).exists():
            raise serializers.ValidationError('Invalid or inactive product.')
        return value


class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity']


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = ['id', 'created_at', 'items']


class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'quantity', 'price_at_purchase']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'order_id', 'total_amount', 'status', 'created_at', 'updated_at', 'items']


class CreateOrderSerializer(serializers.Serializer):
    def create(self, validated_data):
        user = self.context['request'].user

        with transaction.atomic():
            cart, _ = Cart.objects.select_for_update().get_or_create(user=user)
            items = list(cart.items.select_related('product'))
            if not items:
                raise serializers.ValidationError('Cart is empty.')

            total_amount = Decimal('0.00')
            order = Order.objects.create(user=user, total_amount=total_amount)

            order_items = []
            for item in items:
                product = Product.objects.select_for_update().get(pk=item.product_id)
                if product.stock_quantity < item.quantity:
                    raise serializers.ValidationError(
                        f'Insufficient stock for {product.name}. Available: {product.stock_quantity}'
                    )
                product.stock_quantity -= item.quantity
                product.save(update_fields=['stock_quantity'])

                line_total = product.price * item.quantity
                total_amount += line_total
                order_items.append(
                    OrderItem(
                        order=order,
                        product=product,
                        quantity=item.quantity,
                        price_at_purchase=product.price,
                    )
                )

            OrderItem.objects.bulk_create(order_items)
            order.total_amount = total_amount
            order.save(update_fields=['total_amount'])

            cart.items.all().delete()

        return order
