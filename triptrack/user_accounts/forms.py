# user_accounts/forms.py

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from .models import Hire

User = get_user_model()

# ----------------- SignUp Form -----------------
class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User  # use CustomUser
        fields = ['username', 'email', 'password1', 'password2', 'role']  # include role if needed


# ----------------- Hire / Payment Form -----------------
class HireForm(forms.ModelForm):
    class Meta:
        model = Hire
        fields = ['amount', 'start_date', 'end_date']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }

    # automatically assign logged-in user as user_admin
    def save(self, commit=True, user_admin=None):
        hire = super().save(commit=False)
        if user_admin:
            hire.user_admin = user_admin
        if commit:
            hire.save()
        return hire
