from django.db import models
from django.db.models import Sum


class Station(models.Model):
    name = models.CharField(blank=False, null=True, max_length=40)
    location = models.TextField()

    @property
    def estimate_boxes_property(self):
        sum_num_boxes_to_station = Transfer.objects.filter(
            to_station_id=self.id
        ).aggregate(total_boxes=Sum("num_boxes"))["total_boxes"]

        sum_num_boxes_from_station = Transfer.objects.filter(
            from_station_id=self.id
        ).aggregate(total_boxes=Sum("num_boxes"))["total_boxes"]

        # Wenn keine Transfers zur Station vorhanden sind, wird 'None' zurückgegeben. Wir setzen es auf 0
        if sum_num_boxes_to_station is None:
            sum_num_boxes_to_station = 0
        if sum_num_boxes_from_station is None:
            sum_num_boxes_from_station = 0

        return sum_num_boxes_to_station - sum_num_boxes_from_station


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

    class Meta:
        unique_together = ["from_station", "to_station"]

    def __str__(self):
        return f"Transfer from {self.from_station.name} to {self.to_station.name}"
