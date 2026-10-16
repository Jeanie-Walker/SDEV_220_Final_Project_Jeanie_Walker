from django import forms
from .models import Nurse, CATEGORIES, URGENCY_LABELS

DEMO_DAYS =("Mon", "Tue", "Wed")
class LoginForm(forms.Form):
    nurse = forms.ModelChoiceField(
        queryset=Nurse.objects.order_by("name"),
        empty_label="Select your name",
        widget=forms.Select(attrs={"class": "form-select"}),
    )
    day = forms.ChoiceField(
        choices=[("", "Select a day")] + [(d, d) for d in DEMO_DAYS],
        label="Day (demo only)",
        widget=forms.Select(attrs={"class": "form-select"}),
    )

class ReportItemForm(forms.Form):
    category = forms.ChoiceField(
        choices=[("", "Select category")] + [(c, c) for c in CATEGORIES],
        widget=forms.Select(attrs={"class": "form-select"}),
    )
    description = forms.CharField(
        max_length=300,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )

    urgency = forms.ChoiceField(
        choices=[("", "Select urgency")] + list(URGENCY_LABELS.items()),
        widget=forms.Select(attrs={"class": "form-select"}),
    )