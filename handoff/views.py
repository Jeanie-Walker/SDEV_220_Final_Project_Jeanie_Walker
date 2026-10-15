from django.shortcuts import render, redirect

from .forms import LoginForm, ReportItemForm

from .models import Shift, Report, URGENCY_LABELS


def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            nurse = form.cleaned_data["nurse"]
            day = form.cleaned_data["day"]
            request.session["nurse_id"] = nurse.id
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
    
    report = Report.objects.filter(shift__patient=shift.patient).order_by("-created_at").first()
    sections = []

    if report:
        groups = report.items_by_urgency()
        for urgency, items in groups.items():
            sections.append((URGENCY_LABELS[urgency], items))
    
    return render(request, "handoff/patient.html", {"shift": shift, "sections": sections, "report": report})


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