"""取込処理やビジネスロジックをまとめたモジュール"""

from common import const
from collections import (
    defaultdict,
    Counter
)
import csv, io
import pandas as pd
from common.models import (
    PlatForms,
    Works,
    Staffs,
    WorkSeason,
    PlatformInfo
)

def read_csv(upload_file) -> dict:
    """
    CSVファイルを先頭から1行ずつ読み込み配信情報を取り出す.

    Args: upload_file(取込CSVファイル)
    
    Returns: items, platforms_count

    itemsの中身：辞書型リスト{タイトル：[]}
    row[1]:配信日
    row[3]:タイトル
    row[4]:プラットフォーム（複数）
    row[6]:制作会社
    row[7]:URL

    """
    items = defaultdict(list) # 重複タイトルは除く
    try:
        # バイナリファイルを文字列に変換
        # text_file = io.TextIOWrapper(upload_file.file, encoding="utf-8")
        # reader = csv.reader(text_file)
        # 先頭行を飛ばしてCSVデータを読み込む
        df = pd.DataFrame(upload_file)

        for row in df:
            # 対応付けするデータを設定
            title = row[3]
            staff = ("制作会社登録なし" if not row[6] else row[6])
            items[title].append((
                row[1] ,row[4] ,staff ,row[7]
            ))

        print(items)
    except FileExistsError as e:
        print(f"ファイルが存在しません。", e.errno)
        

    return items
    

def is_delivery_cnt(season_delivery_cnt: int) -> bool:
    """
    配信件数入力チェック.（基本配信件数は50件以上）
    """
    return season_delivery_cnt < const.MIN_SEASON_CNT

# トランザクションの制御機能を要調査
def intake_info(item) -> bool:
    """
    配信情報を各種テーブルへ登録

    Args:

    Returns: True：登録成功 False:登録失敗
    
    """
    return True

