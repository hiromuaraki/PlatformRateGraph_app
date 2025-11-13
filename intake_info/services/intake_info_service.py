"""取込処理やビジネスロジックをまとめたモジュール"""

import csv
from common.models import (
    PlatForms,
    Works,
    Staffs,
    WorkSeason,
    PlatformInfo
)

def read_csv(file_path) -> tuple:
    """
    CSVファイルを先頭から1行ずつ読み込み配信情報を取り出す.

    Args:

    Returns:

    """

    return ()
    

def is_delivery_cnt(season_delivery_cnt: int) -> bool:
    """
    配信件数入力チェック.（基本配信件数は50件以上）
    
    Args:

    Returns: True：適切な配信件数 False:不正な配信件数
    
    """

# トランザクションの制御機能を要調査
def intake_info(item) -> bool:
    """
    配信情報を各種テーブルへ登録

    Args:

    Returns: True：登録成功 False:登録失敗
    
    """
    return False

