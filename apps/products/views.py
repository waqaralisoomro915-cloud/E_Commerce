from rest_framework import viewsets
from .models import Product
from .serializers import ProductSerializer
from ..accounts.permissions import (IsAdmin,CanViewProduct)


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


    def get_queryset(self):
        user = self.request.user
        if user.role == 'ADMIN':
            return Product.objects.all()
        return Product.objects.filter(is_active=True)

    def get_permissions(self):
        if self.action in ['destroy', 'update', 'partial_update', 'create']:
            permission_classes = [IsAdmin]
        else:
            permission_classes = [CanViewProduct]
        return [permissions() for permissions in permission_classes]



