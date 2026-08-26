from rest_framework import viewsets
from rest_framework.filters import SearchFilter,OrderingFilter

from .models import Product
from .serializers import ProductSerializer
from ..accounts.permissions import (IsAdmin,CanViewProduct)
from ..paginations.paginations import CustomPagination
from django_filters.rest_framework import DjangoFilterBackend


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = (DjangoFilterBackend,OrderingFilter,SearchFilter,)
    pagination_class = CustomPagination
    filterset_fields=('category','is_active',)
    search_fields=('name','description')
    ordering_fields=('name','price','stock','created_at','updated_at')


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



