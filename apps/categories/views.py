
from rest_framework import viewsets
from .models import Category
from .serializers import CategorySerializer
from rest_framework.permissions import IsAuthenticated
from ..accounts.permissions import IsAdmin, CanViewCategory


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        user = self.request.user
        if user.role == 'ADMIN':
            return Category.objects.all()
        return Category.objects.filter(is_active=True)
    def get_permissions(self):
        if self.action in ['destroy','update','partial_update','create']:
            self.permission_classes = [IsAdmin]
        else:
            self.permission_classes = [CanViewCategory]

        return [permissions() for permissions in self.permission_classes]


