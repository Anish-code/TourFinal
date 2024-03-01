from django import forms
import csv
import pandas as pd


class LocationForm(forms.Form):
    locations = forms.ChoiceField(choices=[])

    def __init__(self, *args, **kwargs):
        super(LocationForm, self).__init__(*args, **kwargs)
        df = pd.read_csv('tourdatas.csv')

        reader = csv.DictReader(df)
        choices = [(row['location'], row['ID']) for row in reader]
        self.fields['locations'].choices = [('', 'Select Location')] + choices
