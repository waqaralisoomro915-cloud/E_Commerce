from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('reviews', views.ReviewViewSet,basename='reviews')
urlpatterns = router.urls
