from django.shortcuts import render, redirect
from .forms import IntakeInfoForm
from django.views.generic import TemplateView
# from django.http import HttpResponse
from common.models import (
    PlatForms,
    PlatformInfo,
    Works,
    Staffs,
    WorkSeason,
)

class IntakeInfoView(TemplateView):
    
    def __init__(self):
        # フォームを設定
        self.params = {
            "success": False,
            "form": IntakeInfoForm(),
            
        }


    def get(self, request):
        """GET時に呼び出し：画面設定"""
        return render(request, "intake_info/index.html", self.params)

    def post(self, request):
        """POST時に呼び出し：取込処理実行"""
        if request.method == "POST":
            self.params["form"] = IntakeInfoForm(request.POST, request.FILES)
            form = self.params["form"]
            if form.is_valid():
                # 検証済みデータの準備
                csv_file = form.cleaned_data['csv_file']
                count = form.cleaned_data['season_delivery_cnt']

                # ToDo CSVファイル取込処理を呼び出す

                # 取込処理成功
                self.params["sccess"] = True
                 # 空のフォームに初期化
                self.params["form"] = IntakeInfoForm()
                return render(request, "intake_info/index.html", self.params)

            else:
                # 入力チェックNGの場合は同じフォームを再表示
                return render(request, "intake_info/index.html", self.params)
        # GETアクセスならindexへリダイレクト
        return redirect("index")
    