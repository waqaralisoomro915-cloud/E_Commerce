from rest_framework.routers import DefaultRouter
from . import views
router = DefaultRouter()
router.register('cartItems',views.CartItemViewSet,basename='cartItem')
urlpatterns = router.urls