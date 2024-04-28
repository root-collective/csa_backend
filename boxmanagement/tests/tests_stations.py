import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from boxmanagement.factories import StationFactory, TransferFactory
from boxmanagement.models import Station


@pytest.mark.django_db
def test_station_list_view():
    # Erstelle ein paar Testdaten
    Station.objects.create(name="Station1", location="Location1")
    Station.objects.create(name="Station2", location="Location2")

    # Erstelle einen APIClient
    client = APIClient()

    # Fordere die Liste der Stationen an
    url = reverse(
        "station-list"
    )  # Annahme: Der Name der URL für die Liste der Stationen ist 'station-list'
    response = client.get(url)

    # Überprüfe, ob die Anfrage erfolgreich war (HTTP-Statuscode 200)
    assert response.status_code == status.HTTP_200_OK

    # Überprüfe, ob die erwarteten Daten in der Antwort sind
    assert len(response.data) == 2
    assert response.data[0]["name"] == "Station1"
    assert response.data[1]["name"] == "Station2"


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
