
from django import forms
from .models import Trek
import csv

class TrekImportForm(forms.Form):
    csv_file = forms.FileField(label='CSV File')

    def process_csv(self):
        if self.is_valid():
            csv_file = self.cleaned_data['csv_file']
            decoded_file = csv_file.read().decode('utf-8').splitlines()
            csv_reader = csv.DictReader(decoded_file)

            for row in csv_reader:
                trek = Trek(
                    trek=row['Trek'],
                    cost=row['Cost'],
                    time=row['Time'],
                    trip_grade=row['Trip Grade'],
                    max_altitude=row['Max Altitude'],
                    accommodation=row['Accommodation'],
                    best_travel_time=row['Best Travel Time'],
                    contact=row['Contact']
                )
                trek.save()
