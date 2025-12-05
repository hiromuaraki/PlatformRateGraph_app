from django.shortcuts import render
from common import utils
from datetime import date
from .service import rate_graph_service as service

# Create your views here.
def chart_view(request):
    """円グラフへ表示させるデータを準備."""
    platform_map = service.get_label_map()
    year, month, day = utils.get_sysdate()
    season_delivery_count = service.get_season_delivery_count(year, month)
    
    # 現在の月日を準備（date型と比較用）
    current_date = date(year, month, day)
    season_data = service.get_current_season_data(current_date)
    # 割合の計算結果のリスト
    calc_rate_map = service.calc_rate_map(season_data, season_delivery_count)
    color_map = service.background_color_map()
    
    # グラフへ表示するデータ準備
    labels = [platform_map[key] for key in calc_rate_map]
    data = [value for value in calc_rate_map.values()]
    color = [color_map[key - 1] for key in calc_rate_map]

    # viewへ表示するデータの設定
    context = {
        "labels": labels,
        "data": data,
        "color": color,
        "version": 1,
        "title": "割合グラフ画面",
    }
    
    return render(request, "rate_graph/chart.html", context)