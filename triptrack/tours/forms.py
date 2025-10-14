from django import forms
from .models import Tour, Hire, Booking

# === Tour Form (For Creators) ===
class TourForm(forms.ModelForm):
    class Meta:
        model = Tour
        fields = ['name', 'description', 'start_date', 'end_date', 'cost', 'location', 'seats_available', 'status']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows':4}),
        }

# === Hire Form (For User Admins) ===
class HireForm(forms.ModelForm):
    class Meta:
        model = Hire
        fields = ['start_date', 'end_date']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }

# === Booking Form (For Enjoyers) ===
class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['tour', 'payment_done']
        widgets = {
            'tour': forms.HiddenInput(),  # Enjoyer selects from dashboard, hidden in form
        }
