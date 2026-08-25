from rest_framework import serializers
from . models import WishList,WishListItem
class WishlistSerializer(serializers.ModelSerializer):
    class Meta:
        model = WishList
        fields ='__all__'
        read_only_fields = ['user']

class WishListItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = WishListItem
        fields ='__all__'
    def validate_wishlist(self,wishlist):
        user = self.context['request'].user
        if user.role != 'ADMIN' and wishlist.user !=user:
            raise serializers.ValidationError('Only ADMIN or CUSTOMER can add wishlists')
        return wishlist

    def validate(self,attrs):
        wishlist = attrs.get('wishlist')
        product = attrs.get('product')
        if WishListItem.objects.filter(wishlist=wishlist,product=product).exists():
            raise serializers.ValidationError('Product already exists')
        return attrs


