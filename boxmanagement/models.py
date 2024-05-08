from datetime import datetime
import pytz
from django.db import models
from django.db.models import Sum
from django.core.exceptions import ObjectDoesNotExist


class Station(models.Model):
    name = models.CharField(blank=False, null=True, max_length=40)
    location = models.TextField()

    @property
    def estimate_boxes_property(self):
        try:
            last_inventory = Inventory.objects.filter(station=self).latest()
            last_inventory_timestamp = last_inventory.timestamp
            last_inventory_num_boxes = last_inventory.num_boxes
        except ObjectDoesNotExist:
            last_inventory_timestamp = datetime(2024, 5, 1, 0, 0, 0, tzinfo=pytz.UTC)
            last_inventory_num_boxes = 0

        sum_num_boxes_to_station = (
            Transfer.objects.filter(timestamp__gte=last_inventory_timestamp)
            .filter(to_station_id=self.id)
            .aggregate(total_boxes=Sum("num_boxes"))["total_boxes"]
        )

        sum_num_boxes_from_station = (
            Transfer.objects.filter(timestamp__gte=last_inventory_timestamp)
            .filter(from_station_id=self.id)
            .aggregate(total_boxes=Sum("num_boxes"))["total_boxes"]
        )

        if sum_num_boxes_to_station is None:
            sum_num_boxes_to_station = 0
        if sum_num_boxes_from_station is None:
            sum_num_boxes_from_station = 0

        return (
            last_inventory_num_boxes
            + sum_num_boxes_to_station
            - sum_num_boxes_from_station
        )


class Transfer(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    num_boxes = models.PositiveIntegerField(default=0)
    from_station = models.ForeignKey(
        Station, on_delete=models.CASCADE, related_name="transfers_from"
    )
    to_station = models.ForeignKey(
        Station, on_delete=models.CASCADE, related_name="transfers_to"
    )
    notes = models.TextField(
        blank=True, null=True, help_text="Additional notes about the transfer"
    )

    def __str__(self):
        return f"Transfer from {self.from_station.name} to {self.to_station.name}"


class Inventory(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    num_boxes = models.PositiveIntegerField(default=0)
    station = models.ForeignKey(
        Station, on_delete=models.CASCADE, related_name="inventory"
    )
    notes = models.TextField(
        blank=True, null=True, help_text="Additional notes about the inventory"
    )

    class Meta:
        get_latest_by = ["timestamp"]

    def __str__(self):
        return f"Inventory at {self.timestamp} in station {self.station.name}: {self.num_boxes} boxes"
