from rest_framework import viewsets
from .serializers import WishlistSerializer, WishListItemSerializer
from .models import WishList,WishListItem
from rest_framework.permissions import IsAuthenticated

class WishlistViewSet(viewsets.ModelViewSet):
    queryset = WishList.objects.all()
    serializer_class = WishlistSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role =='ADMIN':
            return WishList.objects.all()
        return WishList.objects.filter(user=user)
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)



class WishlistItemViewSet(viewsets.ModelViewSet):
    queryset = WishListItem.objects.all()
    serializer_class = WishListItemSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        user = self.request.user
        if user.role =='ADMIN':
            return WishListItem.objects.all()
        return WishListItem.objects.filter(wishlist__user=user)