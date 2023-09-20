from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ImageAPIView, ExpiringLinkView


urlpatterns = [
    path('images_upload/', ImageAPIView.as_view(), name='images'),
    path('image/', ExpiringLinkView.as_view(), name='expiring_link'),
]

