from django.urls import path

from . import views

urlpatterns = [
    path("", views.login_view, name="login"),
    path("patient/", views.patient_view, name="patient"),
    path("report/", views.report_view, name="report"),
    path("preview/", views.preview_view, name="preview"),
]