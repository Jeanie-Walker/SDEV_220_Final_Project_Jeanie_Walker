
CATEGORIES = ("Vitals", "Respiratory", "Nutrition", "PRN meds", "Refills", "Elimination", 
            "Skin", "DME", "New orders", "MD notification", "Function", "Incident", "Other")

URGENCY_LABELS = {1: "Urgent", 2: "Do today", 3: "FYI"}

class Nurse:
    def __init__(self, id, name, credential):
        self.id = id
        self.name = name
        self.credential = credential


class Patient:
    def __init__(self, id, name, adls, continence, diet, code_status, allergies):
        self.id = id
        self.name = name
        self.adls = adls
        self.continence = continence
        self.diet = diet
        self.code_status = code_status
        self.allergies = allergies


class Report:
    def __init__(self, id, shift_id, created_at):
        self.id = id
        self.shift_id = shift_id
        self.created_at = created_at
        self.items = []

    def add_item(self, category, description, urgency):
        self.items.append((category, description, urgency))