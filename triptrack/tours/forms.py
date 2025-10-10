from django import forms
from .models import Tour, Hire

class TourForm(forms.ModelForm):
    class Meta:
        model = Tour
        fields = ['name', 'start_date', 'end_date', 'cost', 'location']

class HireForm(forms.ModelForm):
    class Meta:
        model = Hire
        fields = ['start_date', 'end_date']