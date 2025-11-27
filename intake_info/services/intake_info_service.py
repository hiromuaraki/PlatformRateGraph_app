"""取込処理やビジネスロジックをまとめたモジュール"""

from django.db import transaction
from common import const, utils
from collections import (
    defaultdict,
    Counter
)
import csv, io
from common.models import (
    PlatForms,
    Works,
    Staffs,
    WorkSeason,
    PlatformInfo
)

def read_csv(upload_file) -> tuple:
    """
    CSVファイルを先頭から1行ずつ読み込み配信情報を取り出す.

    Args: upload_file(取込CSVファイル)
    
    Returns: items, delivery_count

    itemsの中身：リスト辞書
    ---------------------
    row[1]:配信日
    row[3]:タイトル
    row[4]:プラットフォーム（複数）
    row[6]:制作会社
    row[7]:URL
    ---------------------

    group_by_count：プラットフォームごとの配信件数
    """
    items = [] # 重複タイトルは除く
    delivery_count = defaultdict(int)
    try:
        # バイナリファイルを文字列に変換
        text_file = io.TextIOWrapper(upload_file.file, encoding="utf-8", newline="\n")
        reader = csv.reader(text_file)
        
        # 先頭行を飛ばしてCSVデータを読み込む
        next(reader)
        
        for row in reader:
            # 対応付けするデータを設定
            staff = ("制作会社登録なし" if not row[6] else row[6].strip())
            # 末尾の改行を削除し追加
            items.append({
                "title": row[3].strip(),
                "delivery_date": row[1].strip(),
                "platform": row[4].strip(),
                "staff": staff,
                "url": row[7].strip()
            })
            # プラットフォームごとの配信件数を集計
            for platform in row[4].split(","):
                if not platform: continue
                # イコールにする為に前後の空白を削除
                delivery_count[platform.strip()] += 1
        print(items)
        print(delivery_count)
    except FileExistsError as e:
        # ある限りCSVファイルは毎期存在するのでこの処理には入らない想定だが保険の処理
        print(f"ファイルが存在しません。", e.errno)
        return None
        
    return items, delivery_count
    

def is_delivery_cnt(season_delivery_cnt: int) -> bool:
    """
    配信件数入力チェック.（基本配信件数は50件以上）
    """
    return season_delivery_cnt < const.MIN_SEASON_CNT


def insert(items: dict, season_delivery_cnt: int, group_by_count: dict) -> bool:
    """
    各テーブルへ新規登録.
    PlatFormsのみ管理者（admin）画面より登録する運用

    get_or_createの挙動
    存在する場合：既存レコード取得
    存在しない場合：新規レコード登録後、登録レコード取得
    """
    # 作品シーズン情報を新規登録 or 既存レコード取得
    work_season, created = WorkSeason.objects.get_or_create(
        season_delivery_cnt=season_delivery_cnt,
        year=item["delivery_date"][:4],
        season=utils.get_season(item["delivery_date"][5:7])
    )
    
    # 既に作品シーズン情報があった場合は登録処理は行わない
    if not created: return False
    
    for item in items:
        # 制作会社を新規登録 or 既存レコード取得
        staff, created = Staffs.objects.get_or_create(
            organization_name=item["staff"]
        )

        # 作品を新規登録 or 既存レコード取得
        work, created = Works.objects.get_or_create(
            staff=staff.id,
            title=item["title"],
            official_url=item["url"]
        )

        # 配信情報一覧をを新規登録 or 既存レコード取得
        platform = PlatForms.objects.filter(name=item["platform"])
        
        # 配信終了日は配信開始日＋3ヶ月に設定
        year, month, day = map(int, item["delivery_date"].split("/"))
        year, month = utils.new_years(year, month)

        platform_info, created = PlatformInfo.objects.get_or_create(
            platform=platform.id,
            work_season=work_season.id,
            delivery_start=item["delivery_date"],
            delivery_end=f"{year}/{month}/{day}",
            delivery_count=group_by_count[item["platform"]]
        )

    return True

def intake_info(items: dict, season_delivery_cnt: int, gropu_by_count: dict) -> bool:
    """CSVデータをテーブルへ取込み."""

    try:
        # [START] トランザクション開始-------------------------------------
        with transaction.atomic():
            success = insert(items, season_delivery_cnt, gropu_by_count)
            raise ValueError("意図的に例外を発生させロールバックさせる。")

        # [END  ] トランザクション終了-------------------------------------

    except Exception as e:
        print("Rollback", e)
        return False
    
    return success

