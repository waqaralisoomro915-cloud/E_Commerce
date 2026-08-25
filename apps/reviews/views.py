from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from ..accounts.permissions import(
CanViewReview,IsAdmin
)


from .models import Review
from .serializers import ReviewSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]
    def get_permissions(self):
        if self.action in ['destroy']:
            permission_classes = [IsAdmin]
        elif self.action in ['update','partial_update','list','retrieve']:
            permission_classes = [CanViewReview]
        else:
            permission_classes = [IsAuthenticated]
        return [
            permission()for permission in permission_classes
        ]


