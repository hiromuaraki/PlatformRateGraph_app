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
    template_name = "intake_info/index.html"
    
    def get_context_data(self, **kwargs):
        """共通のコンテキスト設定"""
        context = super().get_context_data(**kwargs)
        context["form"] = IntakeInfoForm()
        context["success"] = False
        return context

    def get(self, request):
        """GET時に呼び出し：画面設定"""
        context = self.get_context_data()
        return self.render_to_response(context)

    def post(self, request):
        """POST時：フォーム送信処理"""
        form = IntakeInfoForm(request.POST, request.FILES)
        context = self.get_context_data()
        context["form"] = form

        if form.is_valid():
            csv_file = form.cleaned_data["csv_file"]
            count = form.cleaned_data["season_delivery_cnt"]

            # TODO: CSVファイル取込処理呼び出し

            # 成功フラグON & フォーム再初期化
            context["success"] = True
            context["form"] = IntakeInfoForm()

        # 成否に関係なく再描画
        return self.render_to_response(context)
    