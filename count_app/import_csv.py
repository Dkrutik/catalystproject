# import_csv.py

import csv
from django.core.management.base import BaseCommand
from count_app.models import CompanyDataset  # Import your CompanyDataset model


class Command(BaseCommand):
    help = 'Import data from CSV file into the database'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Path to the CSV file')

    def handle(self, *args, **kwargs):
        csv_file_path = kwargs['csv_file']

        with open(csv_file_path, 'r', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                # Create an instance of CompanyDataset model for each row
                company = CompanyDataset(
                    name=row['name'],
                    domain=row['domain'],
                    year_founded=int(row['year founded']),
                    industry=row['industry'],
                    size_range=row['size range'],
                    locality=row['locality'],
                    country=row['country'],
                    linkedin_url=row['linkedin url'],
                    current_employee_estimate=int(row['current employee estimate']),
                    total_employee_estimate=int(row['total employee estimate'])
                )
                # Save the instance to the database
                company.save()

        self.stdout.write(self.style.SUCCESS('Data imported successfully'))
