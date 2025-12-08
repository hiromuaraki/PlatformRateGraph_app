from django.urls import path
from . import views

urlpatterns = [
    path("", views.chart_view, name="chart"),
    path("platform_info/", views.platform_info, name="platform_info"),
]