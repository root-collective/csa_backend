from rest_framework import serializers
from .models import Station, Transfer


class StationSerializer(serializers.ModelSerializer):
    estimate_boxes = serializers.IntegerField(
        source="estimate_boxes_property", read_only=True
    )

    class Meta:
        model = Station
        read_only = ("id", "estimate_boxes")
        fields = ("name", "location") + read_only


class TransferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transfer
        read_only = ("id", "timestamp")
        fields = ("from_station", "to_station", "num_boxes", "notes") + read_only
