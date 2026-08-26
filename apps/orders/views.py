from decimal import Decimal

from django.db import transaction
from django.utils import timezone

from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action

from .models import Order
from .serializers import OrderSerializer, CheckoutSerializer

from ..orderItems.models import OrderItem
from ..cart.models import Cart
from ..products.models import Product
from ..coupons.models import Coupons


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        if user.role == "ADMIN":
            return Order.objects.all()

        return Order.objects.filter(user=user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['post'])
    def checkout(self, request):

        # 1. Validate checkout data
        checkout_serializer = CheckoutSerializer(
            data=request.data,
            context={'request': request}
        )

        checkout_serializer.is_valid(raise_exception=True)

        address = checkout_serializer.validated_data['address']
        coupon = checkout_serializer.validated_data.get('coupon')

        user = request.user

        # Everything below happens as one transaction
        with transaction.atomic():

            # 2. Get user's cart
            cart = Cart.objects.filter(user=user).first()

            if not cart:
                return Response(
                    {"detail": "Cart not found."},
                    status=status.HTTP_404_NOT_FOUND
                )

            # 3. Get cart items
            cart_items = cart.cart_items.select_related(
                'product'
            ).all()

            if not cart_items.exists():
                return Response(
                    {"detail": "Your cart is empty."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # 4. Validate products and stock
            for cart_item in cart_items:

                product = cart_item.product

                if not product.is_active:
                    return Response(
                        {
                            "detail": (
                                f"Product '{product.name}' "
                                "is currently unavailable."
                            )
                        },
                        status=status.HTTP_400_BAD_REQUEST
                    )

                if cart_item.quantity > product.stock:
                    return Response(
                        {
                            "detail": (
                                f"Not enough stock for "
                                f"'{product.name}'. "
                                f"Available stock: {product.stock}."
                            )
                        },
                        status=status.HTTP_400_BAD_REQUEST
                    )

            # 5. Calculate subtotal
            subtotal = Decimal('0.00')

            for cart_item in cart_items:
                product = cart_item.product
                subtotal += product.price * cart_item.quantity

            # 6. Calculate coupon discount
            discount_amount = Decimal('0.00')

            if coupon:

                now = timezone.now()

                # Coupon start date
                if now < coupon.start_date:
                    return Response(
                        {
                            "detail": (
                                "This coupon is not active yet."
                            )
                        },
                        status=status.HTTP_400_BAD_REQUEST
                    )

                # Coupon expiry
                if now > coupon.end_date:
                    return Response(
                        {
                            "detail": "This coupon has expired."
                        },
                        status=status.HTTP_400_BAD_REQUEST
                    )

                # Coupon usage limit
                if (
                    coupon.usage_limit is not None
                    and coupon.used_count >= coupon.usage_limit
                ):
                    return Response(
                        {
                            "detail": (
                                "This coupon has reached "
                                "its usage limit."
                            )
                        },
                        status=status.HTTP_400_BAD_REQUEST
                    )

                # Minimum order amount
                if subtotal < coupon.minimum_order_amount:
                    return Response(
                        {
                            "detail": (
                                f"Minimum order amount for "
                                f"this coupon is "
                                f"{coupon.minimum_order_amount}."
                            )
                        },
                        status=status.HTTP_400_BAD_REQUEST
                    )

                # Percentage discount
                if coupon.discount_type == 'PERCENTAGE':

                    discount_amount = (
                        subtotal *
                        coupon.discount_value /
                        Decimal('100')
                    )

                    # Maximum discount
                    if (
                        coupon.maximum_discount is not None
                        and discount_amount > coupon.maximum_discount
                    ):
                        discount_amount = coupon.maximum_discount

                # Fixed discount
                elif coupon.discount_type == 'FIXED':

                    discount_amount = coupon.discount_value

                    # Discount cannot exceed subtotal
                    if discount_amount > subtotal:
                        discount_amount = subtotal

            # 7. Calculate final total
            total_amount = subtotal - discount_amount

            # 8. Create Order
            order = Order.objects.create(
                user=user,
                address=address,
                coupon=coupon,
                subtotal=subtotal,
                discount_amount=discount_amount,
                total_amount=total_amount,
                status=Order.Status.PENDING
            )

            # 9. Create OrderItems
            for cart_item in cart_items:

                product = cart_item.product
                quantity = cart_item.quantity
                price = product.price

                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=quantity,
                    price=price
                )

                # 10. Reduce stock
                product.stock -= quantity
                product.save(update_fields=['stock'])

            # 11. Increase coupon usage
            if coupon:
                coupon.used_count += 1
                coupon.save(update_fields=['used_count'])

            # 12. Clear cart
            cart_items.delete()

        # 13. Return created order
        serializer = OrderSerializer(
            order,
            context={'request': request}
        )

        return Response(
            {
                "message": "Order created successfully.",
                "order": serializer.data
            },
            status=status.HTTP_201_CREATED
        )

    @action(detail=True, methods=['patch'])
    def update_status(self, request, pk=None):

        order = self.get_object()

        if request.user.role != 'ADMIN':
            return Response(
                {
                    "detail": (
                        "Only admins can update order status."
                    )
                },
                status=status.HTTP_403_FORBIDDEN
            )

        new_status = request.data.get('status')

        if new_status not in Order.Status.values:
            return Response(
                {"detail": "Invalid order status."},
                status=status.HTTP_400_BAD_REQUEST
            )

        allowed_transitions = {
            Order.Status.PENDING: [
                Order.Status.CONFIRMED,
                Order.Status.CANCELLED,
            ],

            Order.Status.CONFIRMED: [
                Order.Status.SHIPPED,
                Order.Status.CANCELLED,
            ],

            Order.Status.SHIPPED: [
                Order.Status.DELIVERED,
            ],

            Order.Status.DELIVERED: [],

            Order.Status.CANCELLED: [],
        }

        if new_status not in allowed_transitions[order.status]:
            return Response(
                {
                    "detail": (
                        f"Order cannot be changed from "
                        f"{order.status} to {new_status}."
                    )
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        order.status = new_status
        order.save(update_fields=['status'])

        return Response(
            {
                "message": "Order status updated successfully.",
                "status": order.status
            },
            status=status.HTTP_200_OK
        )

    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):

        order = self.get_object()

        # Customer can only cancel their own order
        if request.user.role != 'ADMIN' and order.user != request.user:
            return Response(
                {
                    "detail": (
                        "You can only cancel your own order."
                    )
                },
                status=status.HTTP_403_FORBIDDEN
            )

        # Only these statuses can be cancelled
        if order.status not in [
            Order.Status.PENDING,
            Order.Status.CONFIRMED
        ]:
            return Response(
                {
                    "detail": (
                        f"Order cannot be cancelled because "
                        f"its status is {order.status}."
                    )
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        with transaction.atomic():

            # Get order items and their products
            order_items = order.items.select_related(
                'product'
            ).all()

            # Return products to stock
            for order_item in order_items:

                product = order_item.product

                product.stock += order_item.quantity

                product.save(update_fields=['stock'])

            # Cancel order
            order.status = Order.Status.CANCELLED
            order.save(update_fields=['status'])
            if order.coupon and order.coupon.used_count >0:
                order.coupon.used_count -= 1
                order.coupon.save(update_fields=['used_count'])

        return Response(
            {
                "message": "Order cancelled successfully.",
                "status": order.status
            },
            status=status.HTTP_200_OK
        )