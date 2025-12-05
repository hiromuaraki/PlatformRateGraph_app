import common.utils as utils
from django.db.models import Max
from collections import defaultdict
from datetime import date
from common.models import (
    WorkSeason,
    PlatformInfo,
    PlatForms,
    Works,
    Staffs
)

def get_label_map() -> dict:
    """プラットフォーム一覧を取得"""
    return dict(PlatForms.objects.all().order_by("id").values_list("id", "name"))

def get_season_delivery_count(year: int, month: int) -> int:
    """シーズン配信件数を取得"""
    return WorkSeason.objects.filter(
        year=year, season=utils.get_season(int(month)))[0].season_delivery_cnt


def get_current_season_data(current_date: date) -> list:
    """現在のシーズンデータを取得"""
    # platform_id ごとに delivery_count を 1つだけ取得
    qs = PlatformInfo.objects.filter(
        delivery_start__lte=current_date,
        delivery_end__gte=current_date
    ).values("platform_id").annotate(
        delivery_count=Max("delivery_count")
    ).order_by("platform_id")

    return qs


def calc_rate_map(qs: list, season_delivery_count: int) -> dict:
    """プラットフォームごとの配信件数の割合を計算する"""
    dic = defaultdict(float)
    
    for season_data in qs:
        calc_rate = (season_data["delivery_count"] / season_delivery_count) * 100
        dic[season_data["platform_id"]] = calc_rate
    return dict(sorted(dic.items(), key=lambda item: item[1], reverse=True))

def background_color_map():
    """プラットフォームごとの背景色のマップを返す."""
    # プラットフォームが増えた場合は適宜追加
    # 0-indexedに対応-1
    return {
       0: "#171616",
       1: "#f5b642",
       2: "#87a8e0",
       3: "#e3dcda",
       4: "#f26405",
       5: "#d61313",
       6: "#2006c7",
       7: "#73726e",
       8: "#fcde19",
       9: "#f5b642",
       10: "#b5a40b",
       11: "#383e45",
       12: "#56cc49",
       13: "#e8a274",
       14: "#2b2940",
       15: "#FFFFFF"
    }
