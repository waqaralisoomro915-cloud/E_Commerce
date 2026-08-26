from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .serializers import CouponsSerializer
from .models import Coupons
from ..accounts.permissions import IsAdmin


class CouponsViewSet(viewsets.ModelViewSet):
    queryset = Coupons.objects.all()
    serializer_class = CouponsSerializer
    permission_classes = [IsAuthenticated, IsAdmin]