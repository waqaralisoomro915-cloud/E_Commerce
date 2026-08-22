from . import views
from django.urls import path

urlpatterns = [
    path('addresses/',views.addresses,name='addresses'),

]
