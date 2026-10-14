from django.shortcuts import render

from .forms import LoginForm


def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            nurse = form.cleaned_data["nurse"]
            day = form.cleaned_data["day"]
            request.session["nurse_id"] = nurse.id
            request.session["day"] = day
            return render(request, "handoff/login.html", {"form": form, "logged_in": nurse, "day": day})
    else:
        form = LoginForm()

    return render(request, "handoff/login.html", {"form": form})