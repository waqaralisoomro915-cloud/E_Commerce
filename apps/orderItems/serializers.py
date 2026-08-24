from .models import OrderItem
from rest_framework import serializers


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'
        read_only_fields = ['price']

    def validate_order(self, order):
        user = self.context['request'].user

        if user.role != 'ADMIN' and order.user != user:
            raise serializers.ValidationError(
                "You can only add items to your own order."
            )
        if order.status in ['SHIPPED', 'DELIVERED', 'CANCELLED']:
            raise serializers.ValidationError(
                "Items cannot be modified for this order."
            )

        return order

    def validate_quantity(self, quantity):
        if quantity <= 0:
            raise serializers.ValidationError(
                "Quantity must be greater than 0."
            )

        return quantity

    def validate(self, attrs):
        product = attrs['product']
        quantity = attrs['quantity']

        if not product.is_active:
            raise serializers.ValidationError(
                "This product is unavailable."
            )

        if quantity > product.stock:
            raise serializers.ValidationError(
                "The quantity cannot exceed available stock."
            )

        return attrs

    def create(self, validated_data):
        product = validated_data['product']

        validated_data['price'] = product.price

        return super().create(validated_data)