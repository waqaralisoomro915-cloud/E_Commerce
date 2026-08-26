from rest_framework import serializers
from .models import Coupons


class CouponsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Coupons
        fields = '__all__'
        read_only_fields = ['used_count']

    # Validate and normalize the coupon code
    def validate_code(self, code):
        code = code.strip().upper()

        if not code:
            raise serializers.ValidationError(
                "Coupon code cannot be empty."
            )

        return code

    # Make sure the discount value is greater than zero
    def validate_discount_value(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                "Discount value must be greater than 0."
            )

        return value

    # Make sure the minimum order amount is not negative
    def validate_minimum_order_amount(self, value):
        if value < 0:
            raise serializers.ValidationError(
                "Minimum order amount cannot be negative."
            )

        return value

    # Make sure the maximum discount is greater than zero
    def validate_maximum_discount(self, value):
        if value is not None and value <= 0:
            raise serializers.ValidationError(
                "Maximum discount must be greater than 0."
            )

        return value

    # Make sure the usage limit is greater than zero
    def validate_usage_limit(self, value):
        if value is not None and value <= 0:
            raise serializers.ValidationError(
                "Usage limit must be greater than 0."
            )

        return value

    # Validate rules that depend on multiple coupon fields
    def validate(self, attrs):

        discount_type = attrs.get(
            'discount_type',
            getattr(self.instance, 'discount_type', None)
        )

        discount_value = attrs.get(
            'discount_value',
            getattr(self.instance, 'discount_value', None)
        )

        start_date = attrs.get(
            'start_date',
            getattr(self.instance, 'start_date', None)
        )

        end_date = attrs.get(
            'end_date',
            getattr(self.instance, 'end_date', None)
        )

        maximum_discount = attrs.get(
            'maximum_discount',
            getattr(self.instance, 'maximum_discount', None)
        )

        # Make sure percentage discount does not exceed 100%
        if discount_type == Coupons.DiscountType.PERCENTAGE:
            if discount_value > 100:
                raise serializers.ValidationError({
                    'discount_value':
                        'Percentage discount cannot exceed 100%.'
                })

        # Maximum discount only applies to percentage coupons
        elif discount_type == Coupons.DiscountType.FIXED:
            if maximum_discount is not None:
                raise serializers.ValidationError({
                    'maximum_discount':
                        'Maximum discount is only applicable to percentage coupons.'
                })

        # Make sure the end date is after the start date
        if start_date and end_date:
            if end_date <= start_date:
                raise serializers.ValidationError({
                    'end_date':
                        'End date must be after start date.'
                })

        return attrs