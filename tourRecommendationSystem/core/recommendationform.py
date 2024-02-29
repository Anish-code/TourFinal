from django import forms
from core.models import  Tour


class RecommendForm(UserCreationForm):
    category = forms.CharField(widget= forms.TextInput(attrs={"placeholder":"Enter Your Type of destination"}))
    duration = forms.CharField(widget = forms.TextInput(attrs={"placeholder":"How many Days can you spend?"}))
    cost = forms.CharField(widget = forms.TextInput(attrs= {"placeholder":"Enter your estimated budget"}))
    tripGrade = forms.CharField(widget= forms.TextInput(attrs={"placeholder":"Enter the Trip Grade "}))

    
    class Meta:
        
        model = Tour
        fields = ['category', 'duration', 'cost', 'tripGrade']
        




		
		


