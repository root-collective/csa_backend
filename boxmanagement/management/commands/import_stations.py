import yaml
from django.core.management.base import BaseCommand
from boxmanagement.models import Station


class Command(BaseCommand):
    help = "Create stations from a YAML file"

    def add_arguments(self, parser):
        parser.add_argument(
            "yaml_file", type=str, help="Path to the YAML file containing station data"
        )

    def handle(self, *args, **kwargs):
        yaml_file = kwargs["yaml_file"]

        with open(yaml_file, "r") as f:
            data = yaml.safe_load(f)

        for station_data in data:
            name = station_data.get("name")
            if name:
                existing_station = Station.objects.filter(name=name).exists()
                if not existing_station:
                    station = Station.objects.create(**station_data)
                    self.stdout.write(
                        self.style.SUCCESS(
                            f'Successfully created station "{station.name}"'
                        )
                    )
                else:
                    self.stdout.write(
                        self.style.WARNING(
                            f'Station "{name}" already exists, skipping creation'
                        )
                    )
            else:
                self.stdout.write(
                    self.style.ERROR("No name provided for station, skipping creation")
                )
