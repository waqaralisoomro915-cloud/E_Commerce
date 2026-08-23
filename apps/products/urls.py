from . import views
from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register('products', views.ProductViewSet,basename='products')
urlpatterns= router.urls

