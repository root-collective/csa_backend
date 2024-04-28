import pytest
from boxmanagement.models import Station, Transfer
from boxmanagement.factories import StationFactory, TransferFactory


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

