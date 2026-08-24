from .models import CartItems
from rest_framework import serializers

class CartItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItems
        fields = '__all__'


    def validate_cart(self, cart):
        user = self.context['request'].user

        if user.role != 'ADMIN' and cart.user != user:
            raise serializers.ValidationError(
                "You can only add items to your own cart."
            )

        return cart

    def validate_quantity(self, quantity):
        if quantity <= 0:
            raise serializers.ValidationError("The quantity can't be less than zero.")
        return quantity

    def validate(self,attrs):
        product = attrs.get('product')
        quantity = attrs.get('quantity')
        if not product.is_active:
            raise serializers.ValidationError("This product is unavailable.")

        if quantity > product.stock:
            raise serializers.ValidationError("The quantity can't exceed the stock.")

        return attrs


