from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('coupons', views.CouponsViewSet, basename='coupons')
urlpatterns = router.urls