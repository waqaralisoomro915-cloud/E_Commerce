from . import views
from django.urls import path

urlpatterns = [
    path('categories/', views.categories,name='categories'),

]
