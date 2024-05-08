from datetime import datetime
from sqlite3 import Timestamp
import pytz
import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from boxmanagement.factories import InventoryFactory, StationFactory, TransferFactory
from boxmanagement.models import Station


@pytest.mark.django_db
def test_station_list_view():
    # create stations
    Station.objects.create(name="Station1", location="Location1")
    Station.objects.create(name="Station2", location="Location2")

    client = APIClient()

    url = reverse("station-list")
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    assert len(response.data) == 2
    assert response.data[0]["name"] == "Station1"
    assert response.data[1]["name"] == "Station2"


@pytest.mark.django_db
def test_station_post_not_allowed():
    client = APIClient()

    url = reverse("station-list")
    response = client.post(url)

    # Überprüfe, ob die Anfrage mit Status 405 beantwortet wird
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


@pytest.mark.django_db
def test_station_patch_allowed():
    # Erstelle Station
    s = StationFactory()

    client = APIClient()

    new_location = "FarFarAway"
    data = {"location": new_location}
    url = reverse("station-detail", kwargs={"pk": s.id})
    response = client.patch(url, data)

    assert response.status_code == status.HTTP_200_OK
    s.refresh_from_db()
    assert s.location == new_location


@pytest.mark.django_db
def test_station_delete_not_allowed():
    s = StationFactory()

    client = APIClient()

    url = reverse("station-detail", kwargs={"pk": s.id})
    response = client.delete(url)

    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


@pytest.mark.django_db
def test_station_boxestimate_without_transfers():
    source = StationFactory()
    target = StationFactory()
    assert source.estimate_boxes_property == 0
    assert target.estimate_boxes_property == 0


@pytest.mark.django_db
def test_station_boxestimate_with_single_transfers():
    source = StationFactory()
    target = StationFactory()
    transfer = TransferFactory(to_station=target, from_station=source)
    assert source.estimate_boxes_property == -1 * transfer.num_boxes
    assert target.estimate_boxes_property == transfer.num_boxes


@pytest.mark.django_db
def test_station_boxestimate_with_multiple_transfers():
    source = StationFactory()
    target = StationFactory()
    transfer1 = TransferFactory(to_station=target, from_station=source)
    transfer2 = TransferFactory(to_station=target, from_station=source)
    transfered_boxes = transfer1.num_boxes + transfer2.num_boxes
    assert source.estimate_boxes_property == -1 * transfered_boxes
    assert target.estimate_boxes_property == transfered_boxes


@pytest.mark.django_db
def test_station_boxestimate_with_circle_transfers():
    s1 = StationFactory()
    s2 = StationFactory()
    s3 = StationFactory()
    num_boxes = 1
    t1 = TransferFactory(to_station=s2, from_station=s1, num_boxes=num_boxes)
    t2 = TransferFactory(to_station=s3, from_station=s2, num_boxes=num_boxes)
    t3 = TransferFactory(to_station=s1, from_station=s3, num_boxes=num_boxes)
    assert s1.estimate_boxes_property == 0
    assert s2.estimate_boxes_property == 0
    assert s3.estimate_boxes_property == 0


@pytest.mark.django_db
def test_station_boxes_with_inventory():
    station = StationFactory()
    inv1 = InventoryFactory(
        station=station, num_boxes=1000, timestamp=datetime.now(tz=pytz.UTC)
    )
    assert station.estimate_boxes_property == inv1.num_boxes

    t1 = TransferFactory(from_station=station, num_boxes=500)
    station.refresh_from_db()
    assert station.estimate_boxes_property == inv1.num_boxes - t1.num_boxes

    inv2 = InventoryFactory(
        station=station, num_boxes=100, timestamp=datetime.now(tz=pytz.UTC)
    )
    station.refresh_from_db()
    assert station.estimate_boxes_property == inv2.num_boxes

    t2 = TransferFactory(to_station=station, num_boxes=200)
    station.refresh_from_db()
    assert station.estimate_boxes_property == inv2.num_boxes + t2.num_boxes
