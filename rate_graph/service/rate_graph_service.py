import common.utils as utils
from datetime import date
from common.models import (
    WorkSeason,
    PlatformInfo,
    PlatForms,
    Works,
    Staffs
)

def get_current_season_data() -> dict:
    """現在のシーズンデータを辞書型で取得"""
    year, month, day = utils.get_sysdate()
    # date型と比較
    current_date = date(year, month, day)
    # シーズン配信件数を取得
    work_season = WorkSeason.objects.filter(year=year, season=utils.get_season(int(month)))
    
    # delivery_start <= 現在年月日 <= delivery_end＝現在のシーズンデータ
    current_season_data = PlatformInfo.objects.filter(
        delivery_start__lte=current_date,
        delivery_end__gte=current_date
    ).values("platform_id", "delivery_count")

    return current_season_data

def calc_rate_list(current_season_data: dict) -> list:
    """プラットフォームごとの配信件数の割合を計算する"""
    return []
