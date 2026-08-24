from rest_framework.permissions import IsAuthenticated

from .serializers import CartItemsSerializer
from .models import CartItems
from rest_framework import viewsets


class CartItemViewSet(viewsets.ModelViewSet):
    queryset = CartItems.objects.all()
    serializer_class = CartItemsSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        user = self.request.user
        if user.role=='ADMIN':
            return CartItems.objects.all()
        return CartItems.objects.filter(cart__user=user)
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)




