from django.shortcuts import render
from common import utils
from .service import rate_graph_service as service

# Create your views here.
def chart_view(request):
    """円グラフへ表示させるデータを準備"""
    labels = utils.get_label_list()
    season_data = service.get_current_season_data()
    # 割合の計算結果のリスト
    data = service.calc_rate_list(season_data)
    
    # viewへ表示するデータの設定
    context = {
        "labels": labels,
        "data": data,
        "title": "割合グラフ画面",
    }
    
    return render(request, "rate_graph/chart.html", context)