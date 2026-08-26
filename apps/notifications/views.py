from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action

from ..accounts.permissions import IsAdmin
from .serializers import NotificationSerializer
from .models import Notification


class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer

    def get_queryset(self):
        user = self.request.user

        if user.role == "ADMIN":
            return Notification.objects.all()

        return Notification.objects.filter(user=user)

    def get_permissions(self):
        if self.action in ['destroy', 'update', 'partial_update', 'create']:
            self.permission_classes = [IsAdmin]
        else:
            self.permission_classes = [IsAuthenticated]

        return [permission() for permission in self.permission_classes]

    @action(methods=['patch'], detail=True)
    def mark_as_read(self, request, pk=None):
        notification = self.get_object()

        notification.is_read = True
        notification.save(update_fields=['is_read'])

        return Response(
            {
                'message': 'Notification is marked as read',
                'is_read': notification.is_read
            },
            status=status.HTTP_200_OK
        )