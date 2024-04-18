from django.db import models


class Station(models.Model):
    name = models.CharField(blank=False, null=True, max_length=40)
    location = models.TextField()


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
