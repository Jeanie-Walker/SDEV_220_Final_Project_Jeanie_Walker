from django import forms
from .models import Nurse, CATEGORIES, URGENCY_LABELS

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

class ReportItemForm(forms.Form):
    category = forms.ChoiceField(
        choices=[("", "Select category")] + [(c, c) for c in CATEGORIES],
    )
    description = forms.CharField(max_length=300)

    urgency = forms.ChoiceField(
        choices=[("", "Select urgency")] + list(URGENCY_LABELS.items())
    )