# import_stadiums.py

import csv
from django.core.management.base import BaseCommand
from Stadium.models import Stadium

class Command(BaseCommand):
    help = 'Import stadium data from a CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str)

    def handle(self, *args, **kwargs):
        csv_file = kwargs['csv_file']
        try:
            with open(csv_file, mode='r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    # Create a new Stadium record for each row in the CSV
                    Stadium.objects.create(
                        name=row['Stadium'],
                        latitude=row['Latitude'],
                        longitude=row['Longitude'],
                        club=row['Team'],
                        city = row['City'],
                        capacity = row['Capacity']
                    )
                self.stdout.write(self.style.SUCCESS(f'Successfully imported data from {csv_file}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error importing data: {e}'))
