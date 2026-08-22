from django.urls import path
from . import views
urlpatterns = [
    path('coupons/', views.coupons,name='coupons'),
]