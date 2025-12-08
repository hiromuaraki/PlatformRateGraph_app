from django.shortcuts import render
from common import utils
from datetime import date,time
from .service import rate_graph_service as service

INFOS = {}
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
    data = ["{:.2f}".format(value) for value in calc_rate_map.values()]
    color = [color_map[key - 1] for key in calc_rate_map]

    # Chart.jsへ渡すデータ
    context = {
        "labels": labels,
        "data": data,
        "color": color,
        "version": time(), # .pie_chart.jsがキャッシュを読み込まなにようにするための設定
        "title": f"{year}年{utils.get_season(int(month))}アニメ：配信シェア",
        "select": "",
    }
    
    return render(request, "rate_graph/chart.html", context)

def platform_info(request):
    global INFOS
    platform_name = request.GET.get("platform")
    works = None
    select_id = service.get_platform_id(platform_name)
    color = service.background_color_map()
    platform = service.get_platforms(platform_name)
    # 配信情報のキャッシュ管理
    if platform_name in INFOS:
        works = INFOS[platform_name]
    else:
        works = service.get_platform_works(platform_name)
        INFOS[platform_name] = []
        INFOS[platform_name].append(works)

    return render(request, "rate_graph/chart.html", {
        "platform": platform,
        "works": INFOS[platform_name][0],
        "select": platform_name,
        "select_color": color[select_id["id"] - 1]
    })

    


