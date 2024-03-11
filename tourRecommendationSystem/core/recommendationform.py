# forms.py
from django import forms
import csv

class CityForm(forms.Form):
    city = forms.ChoiceField(choices=[])  # Define an empty choice field initially

    def __init__(self, *args, **kwargs):
        super(CityForm, self).__init__(*args, **kwargs)
        
        # Load data from the CSV file and extract unique city names
        cities = set()  # Initialize an empty set to store unique city names
        
        with open('../complete_data.csv', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if 'city' in row:  # Check if 'city' exists in the row
                    cities.add(row['city'])
                else:
                    print(f"Row with missing 'city' column: {row}")  # Print problematic rows
        
        # Populate the choices for the city field with unique city names
        self.fields['city'].choices = [(city, city) for city in cities]
        self.fields['city'].widget.attrs.update({'class': 'form-control'})  # Add form-control class for styling (optional)
