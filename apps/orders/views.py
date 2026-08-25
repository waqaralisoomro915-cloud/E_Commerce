from decimal import Decimal
from ..orderItems.models import OrderItem
from django.db import transaction
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Order
from .serializers import OrderSerializer, CheckoutSerializer
from ..cart.models import Cart
from ..products.models import Product


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
            cart_items = cart.cart_items.select_related('product').all()

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

            # 5. Create Order
            order = Order.objects.create(
                user=user,
                address=address,
                total_amount=Decimal('0.00'),
                status=Order.Status.PENDING
            )

            total_amount = Decimal('0.00')

            # 6. Create OrderItems
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

                # 7. Calculate total
                total_amount += price * quantity

                # 8. Reduce stock
                product.stock -= quantity
                product.save(update_fields=['stock'])

            # 9. Update Order total
            order.total_amount = total_amount
            order.save(update_fields=['total_amount'])

            # 10. Clear cart
            cart_items.delete()

        # 11. Return created order
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
                {"detail": "Only admins can update order status."},
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
                {"detail": "You can only cancel your own order."},
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
            order_items = order.items.select_related('product').all()

            # Return products to stock
            for order_item in order_items:
                product = order_item.product

                product.stock += order_item.quantity

                product.save(update_fields=['stock'])

            # Cancel order
            order.status = Order.Status.CANCELLED
            order.save(update_fields=['status'])

        return Response(
            {
                "message": "Order cancelled successfully.",
                "status": order.status
            },
            status=status.HTTP_200_OK
        )
