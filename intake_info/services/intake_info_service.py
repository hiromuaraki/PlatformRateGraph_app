"""取込処理やビジネスロジックをまとめたモジュール"""

from django.db import transaction
from common import const, utils
from collections import defaultdict
import csv, io
from datetime import date
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
            platforms = row[4].split(",")
            # 末尾の改行を削除し追加
            items.append({
                "title": row[3].strip(),
                "delivery_date": row[1].strip(),
                "platform": platforms,
                "staff": staff,
                "url": row[7].strip()
            })
            # プラットフォームごとの配信件数を集計
            for platform in platforms:
                if not platform: continue
                # 同じデータにする為に前後の空白を削除
                delivery_count[platform.strip()] += 1
        print(delivery_count)
        return items, delivery_count
    except FileExistsError as e:
        # ある限りCSVファイルは毎期存在するのでこの処理には入らない想定だが保険の処理
        print(f"ファイルが存在しません。", e.errno)
        return None


def exists_work_season() -> bool:
    """WorkSeasonの存在チェック"""
    now_year, now_month = utils.get_sysdate()[:2]
    count = WorkSeason.objects.filter(year=now_year, 
                season=utils.get_season(int(now_month)))
    return len(count) == 0


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
        year=items[0]["delivery_date"][:4],
        season=utils.get_season(int(items[0]["delivery_date"][5:7]))
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
            # staff=staff.id,
            staff=staff,
            title=item["title"],
            official_url=item["url"]
        )

        # 配信開始日有の場合のみプラットフォーム情報を登録
        if not item["delivery_date"]: continue
        
        # 配信終了日は配信開始日＋3ヶ月に設定
        year, month, day = map(int, item["delivery_date"].split("/"))
        new_year, new_month = utils.new_years(year, month)

        for p in item["platform"]:
            # 配信情報一覧をを新規登録 or 既存レコード取得
            print(p.strip(), item["title"])
            p_form = p.strip()
            # 配信情報あるデータのみ追加
            if not p_form: continue
            platform_info, created = PlatformInfo.objects.get_or_create(
                platform=PlatForms.objects.filter(name=p_form).first(),
                work=work,
                delivery_start=date(year, month, day),
                delivery_end=date(new_year, new_month, day),
                delivery_count=group_by_count[p_form]
            )
    return True

def intake_info(items: dict, season_delivery_cnt: int, gropu_by_count: dict) -> bool:
    """CSVデータをテーブルへ取込み."""

    try:
        # START トランザクション開始-------------------------------------
        with transaction.atomic():
            return insert(items, season_delivery_cnt, gropu_by_count)
        # END   トランザクション終了-------------------------------------

    except Exception as e:
        print("Rollback", e)
        return False 

