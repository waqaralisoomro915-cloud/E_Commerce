from rest_framework.routers import DefaultRouter
from .views import WishlistViewSet,WishlistItemViewSet

router = DefaultRouter()
router.register('wishlist', WishlistViewSet,basename='wishlist')
router.register('Wishlist_item', WishlistItemViewSet,basename='WishlistItem')
urlpatterns = router.urls