from django.shortcuts import render, redirect
from .forms import IntakeInfoForm
from django.views.generic import TemplateView
from django.contrib import messages
from common import const, utils
from .services import intake_info_service as service

class IntakeInfoView(TemplateView):
    template_name = "intake_info/index.html"
    
    def get_context_data(self, **kwargs):
        """共通のコンテキスト設定"""
        context = super().get_context_data(**kwargs)
        context["form"] = IntakeInfoForm()
        context["title"] = "配信情報取込"
        context["is_take"] = (False if service.exists_work_season() else True)
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
            season_delivery_cnt = form.cleaned_data["season_delivery_cnt"]

            # シーズンの配信件数をチェック
            if service.is_delivery_cnt(season_delivery_cnt):
                messages.warning(request, f"最小の配信件数は[{const.MIN_SEASON_CNT}]件～です。")
                return self.render_to_response(context)
            
            # 配信情報/配信件数を取り出す
            items, group_by_count = service.read_csv(csv_file)
                
            # 取込処理の開始
            if (service.intake_info(items, season_delivery_cnt, group_by_count)):
                # フォーム再初期化
                context["form"] = IntakeInfoForm()
                context["is_take"] = True
                messages.success(request, "✅取込が完了しました。")
            else:
                messages.warning(request, "✖既に取込済みです。")

        # 成否に関係なく再描画
        return self.render_to_response(context)
    