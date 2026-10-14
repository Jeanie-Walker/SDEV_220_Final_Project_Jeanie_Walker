from django import forms
from .models import Nurse

DEMO_DAYS =("Mon", "Tue", "Wed")

class LoginForm(forms.Form):
    nurse = forms.ModelChoiceField(
        queryset=Nurse.objects.order_by("name"),
        empty_label="Select your name",
    )
    day = forms.ChoiceField(
        choices=[("", "Select a day")] + [(d, d) for d in DEMO_DAYS],
        label="Day (demo only)",
    )