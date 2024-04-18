# Generated by Django 5.0.4 on 2024-04-18 18:51

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Station",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=40, null=True)),
                ("location", models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name="Transfer",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("timestamp", models.DateTimeField()),
                ("num_boxes", models.PositiveIntegerField(default=0)),
                (
                    "notes",
                    models.TextField(
                        blank=True,
                        help_text="Additional notes about the transfer",
                        null=True,
                    ),
                ),
                (
                    "from_station",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="transfers_from",
                        to="boxmanagement.station",
                    ),
                ),
                (
                    "to_station",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="transfers_to",
                        to="boxmanagement.station",
                    ),
                ),
            ],
            options={
                "unique_together": {("from_station", "to_station")},
            },
        ),
    ]