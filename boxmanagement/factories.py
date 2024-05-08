import factory
from .models import Station, Transfer, Inventory


class StationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Station

    name = factory.Faker("word")
    location = factory.Faker("address")


class TransferFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Transfer

    timestamp = factory.Faker("date_time")
    num_boxes = factory.Faker("random_int", min=1, max=100)
    from_station = factory.SubFactory(StationFactory)
    to_station = factory.SubFactory(StationFactory)
    notes = factory.Faker("text")


class InventoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Inventory

    timestamp = factory.Faker("date_time")
    num_boxes = factory.Faker("random_int", min=1, max=100)
    station = factory.SubFactory(StationFactory)
    notes = factory.Faker("text")
