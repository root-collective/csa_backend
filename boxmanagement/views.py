from rest_framework import viewsets
from .models import Station, Transfer, Inventory
from .serializers import StationSerializer, TransferSerializer, InventorySerializer


class StationViewSet(viewsets.ModelViewSet):
    http_method_names = ["get", "patch", "head"]
    queryset = Station.objects.all()
    serializer_class = StationSerializer


class TransferViewSet(viewsets.ModelViewSet):
    queryset = Transfer.objects.all()
    serializer_class = TransferSerializer


class InventoryViewSet(viewsets.ModelViewSet):
    http_method_names = ["get", "post", "head"]
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer
