from rest_framework import serializers
from .models import Order

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