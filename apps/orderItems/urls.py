from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('orderItems', views.OrderItemsViewSet, basename='orderItems')
urlpatterns = router.urls