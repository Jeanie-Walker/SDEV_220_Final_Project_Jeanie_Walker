"""Demo data loaded to the database, can be reloaded to reset demo"""

from datetime import datetime
from django.core.management.base import BaseCommand
from django.utils import timezone
from handoff.models import Nurse, Patient, Shift, Report
from django.contrib.sessions.models import Session


# Nurse name, credential
NURSES = [
    ("Francis Smith", "RN"),
    ("Alex Walls", "LPN"),
    ("Pilar Flores", "RN"),
    ("Gail Robinson", "LPN"),
    ("Samantha Couch", "LPN"),
    ("Amanda Richards", "RN"),
    ("Whitni Tailor", "LPN"),
    ("Ayesha Johnson", "RN"),
]

# Patient name, ADL status, continence status, diet type, code status, allergies
PATIENTS = [
    ("Linda Williams", "Total assist", "Incontinent of B&B", "Enteral feeds, NPO", "DNR", "NKA"),
    ("Sherry Banks", "Mod assist", "Incontinent of bladder", "Mech soft NAS", "Full Code", "Statins"),
    ("Bethany Carter", "Mod(toileting, bathing, mobility) min(eating)", "Continent", "Regular", "Full Code", "Penicillin")
]

# Assigned shifts using nurse number, patient number, what day the nurse has the patient, and the shift assigned
SHIFTS = [
    (1, 1, "Mon", "day"),
    (1, 1, "Tue", "day"),
    (1, 1, "Wed", "day"),
    (4, 1, "Mon", "night"),
    (2, 1, "Tue", "night"),
    (2, 1, "Wed", "night"),
    (3, 2, "Mon", "day"),
    (3, 2, "Tue", "day"),
    (5, 2, "Wed", "day"),
    (5, 2, "Mon", "night"),
    (6, 2, "Tue", "night"),
    (6, 2, "Wed", "night"),
    (7, 3, "Mon", "day"),
    (7, 3, "Tue", "day"),
    (8, 3, "Wed", "day"),
    (8, 3, "Mon", "night"),
    (4, 3, "Tue", "night"),
    (4, 3, "Wed", "night"),
    (4, 1, "Sun", "night"),
    (5, 2, "Sun", "night"),
    (8, 3, "Sun", "night")
]

# patient number, date, and time for Sunday night demo data
REPORTS = [
    (1, "2026-10-05 06:45"),
    (2, "2026-10-05 06:45"),
    (3, "2026-10-05 06:45")
]

# demo patient report with report number, category, description and urgency
REPORT_ITEMS = [
    # Linda's report (report 1)
    (1, "Skin", "Redness on sacrum, repositioned q2h, monitor", 1),
    (1, "Nutrition", "Tolerated well, no residual", 3),
    (1, "Refills", "Refill needed on Keppra", 2),
    (1, "Elimination", "Large, formed", 3),
    (1, "PRN meds", "Applied Calazime to sacrum per order", 3),

    # Sherry's report (report 2)
    (2, "Incident", "Follow up fall, continues neuro checks, currently q2hrs until 1000", 1),
    (2, "New orders", "neuro checks, see order", 2),
    (2, "New orders", "Colace by mouth twice daily for constipation", 2),
    (2, "Elimination", "Small, hard", 3),

    # Bethany's report (report3)
    (3, "MD notification", "Notify MD about continued insomnia", 2),
    (3, "Respiratory", "Lungs noted with rhonchi, cleared with cough assist", 3),
    (3, "Function", "Pt noted to be irritable, refused care x2", 3),
    (3, "Other", "Pt c/o headache in the night but refused PRN pain reliever", 3),
    (3, "Elimination", "No BM this shift", 3)

]

class Command(BaseCommand):
    help = "Reset database to demo data"

    def handle(self, *args, **options):
        """Deletes all demo data and sessions, then reloads with starting seed data"""
        # deleting nurses and patients removes their shifts, reports, and items
        Nurse.objects.all().delete()
        Patient.objects.all().delete()
        Session.objects.all().delete()

        # nurses and patients
        nurses = [Nurse.objects.create(name=n, credential=c) for n, c in NURSES]

        patients = [Patient.objects.create(name=p[0], adls=p[1], continence=p[2], 
                    diet=p[3], code_status=p[4], allergies=p[5])
                    for p in PATIENTS]

        # shifts
        for nurse_num, patient_num, day, shift_type in SHIFTS:
            Shift.objects.create(nurse=nurses[nurse_num - 1],
                                patient=patients[patient_num - 1],
                                day=day, shift_type=shift_type)

        # reports
        reports = []
        for patient_num, written_at in REPORTS:
            shift = Shift.objects.get(patient=patients[patient_num - 1], day="Sun", shift_type="night")
            created_at = timezone.make_aware(datetime.strptime(written_at, "%Y-%m-%d %H:%M"))
            reports.append(Report.objects.create(shift=shift, created_at=created_at))

        # items
        for report_num, category, description, urgency in REPORT_ITEMS:
            reports[report_num - 1].add_item(category, description, urgency)

        self.stdout.write(self.style.SUCCESS("demo data seeded"))