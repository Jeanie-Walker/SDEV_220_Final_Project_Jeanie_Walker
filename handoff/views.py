from django.shortcuts import render, redirect
from .forms import LoginForm, ReportItemForm
from .models import Shift, Report, URGENCY_LABELS
from django.utils import timezone
from datetime import date, time, datetime, timedelta

DEMO_DATES = {"Mon": date(2026, 10, 5), "Tue": date(2026, 10, 6), "Wed": date(2026, 10, 7)}

DAY_ORDER = ["Sun", "Mon", "Tue", "Wed"]

def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            nurse = form.cleaned_data["nurse"]
            day = form.cleaned_data["day"]
            request.session["nurse_id"] = nurse.id
            request.session["nurse_name"] = str(nurse)
            request.session["day"] = day
            return redirect("patient")
    else:
        form = LoginForm()

    return render(request, "handoff/login.html", {"form": form})


def patient_view(request):
    nurse_id = request.session.get("nurse_id")
    day = request.session.get("day")
    if not nurse_id or not day:
        return redirect("login")
    
    shift = Shift.objects.filter(nurse_id=nurse_id, day=day).first()

    
    if not shift:
        return render(request, "handoff/no_shift.html", {"day": day})

    if shift.shift_type == "day":
        prev_day = DAY_ORDER[DAY_ORDER.index(shift.day) - 1]
        prev_type = "night"

    else:
        prev_day = shift.day
        prev_type = "day"

    prev_shift = Shift.objects.filter(patient=shift.patient, day=prev_day, shift_type=prev_type).first()
    missed = prev_shift is not None and not Report.objects.filter(shift=prev_shift).exists()
    
    report = Report.objects.filter(shift__patient=shift.patient).order_by("-created_at").first()
    sections = []

    if report:
        groups = report.items_by_urgency()
        for urgency, items in groups.items():
            sections.append((URGENCY_LABELS[urgency], items))
    
    return render(request, "handoff/patient.html", {"shift": shift, "sections": sections, "report": report, "missed": missed})


def report_view(request):
    nurse_id = request.session.get("nurse_id")
    day = request.session.get("day")
    if not nurse_id or not day:
        return redirect("login")
    shift = Shift.objects.filter(nurse_id=nurse_id, day=day).first()
        
    if not shift:
        return redirect("patient")

    draft = request.session.get("draft", [])

    if request.method == "POST":
        if "remove" in request.POST:
            index = int(request.POST["remove"])
            draft.pop(index)
            request.session["draft"] = draft
            return redirect("report")
        form = ReportItemForm(request.POST)
        if form.is_valid():
            category = form.cleaned_data["category"]
            description = form.cleaned_data["description"]
            urgency = int(form.cleaned_data["urgency"])
            draft.append({"category": category, "description": description, "urgency": urgency})
            request.session["draft"] = draft
            return redirect("report")
    else:
        form = ReportItemForm()
        
    return render(request, "handoff/report.html", {"form": form, "draft": draft, "shift": shift})

def preview_view(request):
    nurse_id = request.session.get("nurse_id")
    day = request.session.get("day")
    if not nurse_id or not day:
        return redirect("login")
    shift = Shift.objects.filter(nurse_id=nurse_id, day=day).first()
            
    if not shift:
        return redirect("patient")
    
    draft = request.session.get("draft", [])
    if not draft:
        return redirect("report")

    groups = {1: [], 2: [], 3: []}
    for item in draft:
        groups[item["urgency"]].append(item)

    sections = []
    
    for urgency, items in groups.items():
        sections.append((URGENCY_LABELS[urgency], items))

    return render(request, "handoff/preview.html", {"shift": shift, "sections": sections})

    
def save_view(request):
    if request.method != "POST":
        return redirect("preview")

    nurse_id = request.session.get("nurse_id")
    day = request.session.get("day")
    if not nurse_id or not day:
        return redirect("login")

    shift = Shift.objects.filter(nurse_id=nurse_id, day=day).first()
    if not shift:
        return redirect("patient")

    draft = request.session.get("draft", [])
    if not draft:
        return redirect("report")

    if Report.objects.filter(shift=shift).exists():
        return redirect("patient")

    report_date = DEMO_DATES[shift.day]
    if shift.shift_type == "day":
        report_time = datetime.combine(report_date, time(18, 45))
    else:
        report_time = datetime.combine(report_date + timedelta(days=1), time(6, 45))

    report = Report.objects.create(shift=shift, created_at=timezone.make_aware(report_time))
    for item in draft:
        report.add_item(item["category"], item["description"], item["urgency"])

    request.session["draft"] = []
    return redirect("patient")

def logout_view(request):
    request.session.flush()
    return redirect("login")