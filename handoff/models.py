from django.db import models


CATEGORIES = ("Vitals", "Respiratory", "Nutrition", "PRN meds", "Refills", "Elimination", 
            "Skin", "DME", "New orders", "MD notification", "Function", "Incident", "Other")

URGENCY_LABELS = {1: "Urgent", 2: "Do today", 3: "FYI"}

class Nurse(models.Model):
    name = models.CharField(max_length=100)
    credential = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name}, {self.credential}"
    
class Patient(models.Model):
    name = models.CharField(max_length=100)
    adls = models.CharField(max_length=100)
    continence = models.CharField(max_length=100)
    diet = models.CharField(max_length=100)
    code_status = models.CharField(max_length=100)
    allergies = models.CharField(max_length=100)


class Shift(models.Model):
    nurse = models.ForeignKey(Nurse, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    day = models.CharField(max_length=3)
    shift_type = models.CharField(max_length=5)

class Report(models.Model):
    shift = models.OneToOneField(Shift, on_delete=models.CASCADE, related_name="report")
    created_at = models.DateTimeField()

    def add_item(self, category, description, urgency):
        self.items.create(category=category, description=description, urgency=urgency)
    
    def items_by_urgency(self):
        groups = {1: [], 2: [], 3: []}
        for item in self.items.all():
            groups[item.urgency].append(item)
        return groups



class ReportItem(models.Model):
    report = models.ForeignKey(Report, on_delete=models.CASCADE, related_name="items")
    category = models.CharField(max_length=100)
    description = models.CharField(max_length=300)
    urgency = models.IntegerField()

