from django.urls import path
from .views import IntakeInfoView

urlpatterns = [
    path("", IntakeInfoView.as_view(), name="form"),
]