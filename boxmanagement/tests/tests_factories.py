import pytest
from boxmanagement.models import Station, Transfer, Inventory
from boxmanagement.factories import StationFactory, TransferFactory, InventoryFactory


@pytest.mark.django_db
def test_station_factory():
    s = StationFactory()

    db_station = Station.objects.get(id=1)
    assert s.name == db_station.name


@pytest.mark.django_db
def test_transfer_factory():
    t = TransferFactory()

    db_transfer = Transfer.objects.get(id=1)
    assert t.num_boxes == db_transfer.num_boxes

    assert Station.objects.count() == 2


@pytest.mark.django_db
def test_inventory_factory():
    i = InventoryFactory()

    db_inventory = Inventory.objects.get(id=1)
    assert i.num_boxes == db_inventory.num_boxes

    assert Station.objects.count() == 1
