import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from boxmanagement.factories import InventoryFactory


@pytest.mark.django_db
def test_inventory_view_get():
    i = InventoryFactory()

    client = APIClient()

    url = reverse("inventory-list")
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    assert len(response.data) == 1
    assert response.data[0]["station"] == i.station.id
