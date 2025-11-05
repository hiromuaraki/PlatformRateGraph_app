from django.shortcuts import render
from .forms import IntakeInfo
# from django.http import HttpResponse
from common.models import (
    PlatForms,
    PlatformInfo,
    Works,
    Staffs,
    WorkSeason,
)

# Create your views here.
def index(request):
    """配信情報取り込み画面"""
    form = IntakeInfo()
    return render(request, 'intake_info/index.html', {'form': form})