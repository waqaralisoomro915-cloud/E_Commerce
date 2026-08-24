from rest_framework.permissions import IsAuthenticated

from .models import Cart
from .serializers import CartSerializer
from rest_framework import viewsets

class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        user = self.request.user
        if user.role =='ADMIN':
            return Cart.objects.all()
        return Cart.objects.filter(user=self.request.user)
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)