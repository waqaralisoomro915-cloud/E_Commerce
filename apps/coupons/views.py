from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter,OrderingFilter
from ..paginations.paginations import CustomPagination
from .serializers import CouponsSerializer
from .models import Coupons



class CouponsViewSet(viewsets.ModelViewSet):
    queryset = Coupons.objects.all()
    serializer_class = CouponsSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination
    filter_backends = (DjangoFilterBackend,SearchFilter,OrderingFilter)
    filterset_fields = ('code','is_active')
    search_fields = ('code',)
    ordering_fields = ('code','discount_type','discount_value','minimum_order_amount','maximum_order_amount','start_date','end_date','usage_limit','created_at','updated_at','updated_at')
