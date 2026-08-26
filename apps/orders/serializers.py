from rest_framework import serializers
from .models import Order
from ..addresses.models import Address
from ..coupons.models import Coupons


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

    def validate_address(self, address):
        user = self.context['request'].user

        if user.role != 'ADMIN' and address.user != user:
            raise serializers.ValidationError(
                "You can only use your own address."
            )

        return address


class CheckoutSerializer(serializers.Serializer):
    address = serializers.PrimaryKeyRelatedField(
        queryset=Address.objects.all()
    )
    coupon = serializers.CharField(required=False,allow_blank=True)

    def validate_address(self, address):
        user = self.context['request'].user

        if address.user != user:
            raise serializers.ValidationError(
                "You can only use your own address."
            )

        return address
    def validate_coupon(self, coupon):

        if not coupon:
            return None

        coupon = Coupons.objects.filter(
            code__iexact=coupon,
            is_active=True
        ).first()

        if not coupon:
            raise serializers.ValidationError(
                "Invalid or inactive coupon."
            )

        return coupon