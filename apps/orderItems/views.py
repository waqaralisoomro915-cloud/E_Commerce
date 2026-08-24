from rest_framework import viewsets
from . models import OrderItem
from .serializers import OrderItemSerializer
from rest_framework.permissions import IsAuthenticated

class OrderItemsViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role=='ADMIN':
            return OrderItem.objects.all()
        return OrderItem.objects.filter(order__user=user)


