from rest_framework import serializers
from .models import Payment


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'
        read_only_fields = [
            'amount',
            'status',
            'transaction_id',
            'created_at',
            'updated_at',
        ]

    def validate_order(self, order):
        user = self.context['request'].user

        # Customer can only use their own order
        if user.role != 'ADMIN' and order.user != user:
            raise serializers.ValidationError(
                "You can only make payment for your own order."
            )

        # Don't create another payment for an already paid order
        if hasattr(order, 'payment'):
            raise serializers.ValidationError(
                "This order already has a payment."
            )

        return order

    def validate_payment_method(self, payment_method):
        if payment_method != 'COD':
            raise serializers.ValidationError(
                "Only Cash on Delivery is currently available."
            )

        return payment_method

    def create(self, validated_data):
        order = validated_data['order']

        validated_data['amount'] = order.total_amount
        validated_data['status'] = 'PENDING'

        return super().create(validated_data)