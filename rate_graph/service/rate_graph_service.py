import common.utils as utils
from django.db.models import Max, Count
from collections import defaultdict
from datetime import date
from common.models import (
    WorkSeason,
    PlatformInfo,
    PlatForms,
    Works
)

def get_label_map() -> dict:
    """プラットフォーム一覧を取得"""
    return dict(PlatForms.objects.all().order_by("id").values_list("id", "name"))

def get_season_delivery_count(year: int, month: int) -> int:
    """シーズン配信件数を取得"""
    qs = WorkSeason.objects.filter(
        year=year, season=utils.get_season(int(month))).first()
    if qs is None:
        return 0
    return qs.season_delivery_cnt


def get_current_season_data(current_date: date) -> dict:
    """現在のシーズンデータを取得"""
    qs = PlatformInfo.objects.filter(batch_key=utils.get_current_batch_key(current_date))
    result = defaultdict(int)
    st_cnt = set()
    for p in qs:
        st_cnt.add((p.platform_id, p.delivery_count))
    
    for p_id, delivery_count in st_cnt:
        # delivery_count は 1作品ごとに1度だけ足す
        result[p_id] += delivery_count

    return result


def get_platforms(platform_name: str):
    """プラットフォーム情報を取得."""
    return PlatForms.objects.filter(name=platform_name).first()

def get_platform_id(platform_name: str):
    """プラットフォームのIDを取得."""
    return PlatForms.objects.filter(name=platform_name).values("id").first()


def get_platform_works(platform__name):
    """プラットフォームごとの配信情報を配信日が早い順に取得."""
    sysdate = utils.get_sysdate()
    current_date = date(sysdate[0], sysdate[1], sysdate[2])
    return Works.objects.filter(
        batch_key=utils.get_current_batch_key(current_date),
        platform_infos__platform__name=platform__name,
        platform_infos__is_deleted=False
    ).distinct().order_by("platform_infos__delivery_start")


def calc_rate_map(qs: dict, season_delivery_count: int) -> dict:
    """プラットフォームごとの配信件数の割合を計算する"""
    dic = defaultdict(float)
    
    for key, delivery_count in qs.items():
        calc_rate = (delivery_count / season_delivery_count) * 100
        dic[key] = calc_rate
    return dict(sorted(dic.items(), key=lambda item: item[1], reverse=True))

def background_color_map() -> dict:
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
       15: "#FFFFFF",
       16: "#ab0c2e",
    }
