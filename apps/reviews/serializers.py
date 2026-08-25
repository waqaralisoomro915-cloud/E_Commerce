from rest_framework import serializers

from .models import Review
from ..orders.models import Order


class ReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ['user']

    def validate_rating(self, rating):
        if rating < 1 or rating > 5:
            raise serializers.ValidationError(
                "Rating must be between 1 and 5."
            )

        return rating

    def validate_order(self, order):
        user = self.context['request'].user

        if user.role != 'ADMIN' and order.user != user:
            raise serializers.ValidationError(
                "You can only review your own order."
            )

        if order.status != Order.Status.DELIVERED:
            raise serializers.ValidationError(
                "You can only review a delivered order."
            )

        return order

    def validate(self, attrs):
        product = attrs['product']
        order = attrs['order']
        user = self.context['request'].user

        # Check that the product was actually purchased
        if not order.items.filter(product=product).exists():
            raise serializers.ValidationError(
                "This product does not belong to this order."
            )

        # Prevent duplicate review
        if Review.objects.filter(
            user=user,
            product=product,
            order=order
        ).exists():
            raise serializers.ValidationError(
                "You have already reviewed this product for this order."
            )

        return attrs

    def create(self, validated_data):
        user = self.context['request'].user

        return Review.objects.create(
            user=user,
            **validated_data
        )