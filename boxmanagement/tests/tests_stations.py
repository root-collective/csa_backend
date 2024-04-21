import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
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
