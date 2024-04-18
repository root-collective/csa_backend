from django.urls import path, include
from rest_framework.routers import DefaultRouter

from boxmanagement.views import StationViewSet, TransferViewSet

# Create a router and register our ViewSets with it.
router = DefaultRouter()
router.register(r"station", StationViewSet, basename="station")
router.register(r"transfer", TransferViewSet, basename="transfer")

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path("", include(router.urls)),
]
