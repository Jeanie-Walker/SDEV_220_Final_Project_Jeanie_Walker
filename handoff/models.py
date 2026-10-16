"""Database models for Next Shift: nurses, patients, shifts, reports, and report items."""

from django.db import models

# List items for categories
CATEGORIES = ("Vitals", "Respiratory", "Nutrition", "PRN meds", "Refills", "Elimination", 
            "Skin", "DME", "New orders", "MD notification", "Function", "Incident", "Other")

# Dictionary for urgency labels
URGENCY_LABELS = {1: "Urgent", 2: "Do today", 3: "FYI"}

class Nurse(models.Model):
    """Nurse list setup"""
    name = models.CharField(max_length=100)
    credential = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name}, {self.credential}"

class Patient(models.Model):
    """Patient card setup"""
    name = models.CharField(max_length=100)
    adls = models.CharField(max_length=100)
    continence = models.CharField(max_length=100)
    diet = models.CharField(max_length=100)
    code_status = models.CharField(max_length=100)
    allergies = models.CharField(max_length=100)

class Shift(models.Model):
    """Shift assignment tying one nurse to one patient on one day"""
    nurse = models.ForeignKey(Nurse, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    day = models.CharField(max_length=3)
    shift_type = models.CharField(max_length=5)

class Report(models.Model):
    """One handoff report written for one shift"""
    shift = models.OneToOneField(Shift, on_delete=models.CASCADE, related_name="report")
    created_at = models.DateTimeField()

    def add_item(self, category, description, urgency):
        """Add item to report items"""
        self.items.create(category=category, description=description, urgency=urgency)

    def items_by_urgency(self):
        """Return report items grouped by urgency"""
        groups = {1: [], 2: [], 3: []}
        for item in self.items.all():
            groups[item.urgency].append(item)
        return groups



class ReportItem(models.Model):
    """Single line item in a report"""
    report = models.ForeignKey(Report, on_delete=models.CASCADE, related_name="items")
    category = models.CharField(max_length=100)
    description = models.CharField(max_length=300)
    urgency = models.IntegerField()

