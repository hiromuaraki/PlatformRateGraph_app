from django.shortcuts import render
from .forms import IntakeInfoForm
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
    success = False
    if request.method == "POST":
        form = IntakeInfoForm(request.POST, request.FILES)
        if form.is_valid():
            # CSVファイルと件数を取得
            # 検証済みデータの準備
            csv_file = form.cleaned_data['csv_file']
            count = form.cleaned_data['season_delivery_cnt']
            success = True
    else:
        form = IntakeInfoForm()
    return render(request, "intake_info/index.html", {"form": form, "success": success})