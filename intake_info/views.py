from django.shortcuts import render, redirect
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
    """画面設定"""
    form = IntakeInfoForm()
    return render(request, "intake_info/index.html", {"form": form})


def form(request):
    """取込処理実行"""
    success = False
    if request.method == "POST":
        form = IntakeInfoForm(request.POST, request.FILES)
        if form.is_valid():
            # 検証済みデータの準備
            csv_file = form.cleaned_data['csv_file']
            count = form.cleaned_data['season_delivery_cnt']
            
            # ToDo CSVファイル取込処理を呼び出す
            
            # 取込処理成功
            success = True
            return render(request, "intake_info/index.html", {"form": IntakeInfoForm(), "success": success}) # 空のフォームに初期化
        
        else:
            # 入力チェックNGの場合は同じフォームを再表示
            return render(request, "intake_info/index.html", {"form": form})
    # GETアクセスならindexへリダイレクト
    return redirect("index")