from django.db import connection
from datetime import date
import os, django

# Django環境でtruncate.pyを読み込む為の設定
# modelを読み込む前にこの設定しないとプロジェクトのsettings.pyのINSTALLED_APPを見に行きエラーとなる。
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "PlatformRateGraph_app.settings")
django.setup()


from common.models import  (
    WorkSeason,
    Staffs,
    Works,
    PlatformInfo,
    PlatForms
)

import common.utils as utils

# save as dump_platforminfo.py
from django.core import serializers

def batch_script():
    """四半期ごとに実行するバッチスクリプト"""
    sysdate = utils.get_sysdate()
    current_date = date(sysdate[0],sysdate[1], sysdate[2])
    batch_key = utils.get_current_batch_key(current_date)
    
    # 関連 Works と Staffs を取得
    platform_infos = PlatformInfo.objects.filter(batch_key=batch_key)
    
    works_ids = platform_infos.values_list("work_id", flat=True).distinct()
    works = Works.objects.filter(id__in=works_ids, batch_key=batch_key)
    
    staffs_ids = works.values_list("staff_id", flat=True).distinct()
    staffs = Staffs.objects.filter(id__in=staffs_ids)
    
    work_seasons = WorkSeason.objects.filter(batch_key=batch_key)

    platforms = PlatForms.objects.all()
    # すべてをまとめる
    all_objs = list(platforms) + list(work_seasons) + list(staffs) + list(works) + list(platform_infos)
    
    with open(f"data/add_{batch_key}.json", "w") as f:
        f.write(serializers.serialize("json", all_objs, indent=2))


def truncate():
    """tableのデータを全て削除するスクリプト（py truncate.pyで削除実行）"""
    # モデルクラス → テーブル名に変換
    table_names = [WorkSeason._meta.db_table,
                   PlatformInfo._meta.db_table,
                   Works._meta.db_table,
                   Staffs._meta.db_table]
    for table_name in table_names:
        with connection.cursor() as cursor:
            cursor.execute(f'DELETE FROM {table_name};')
            # 次に挿入されるIDが 1から再スタート します
            cursor.execute(f'DELETE FROM sqlite_sequence WHERE name="{table_name}";')
        print((f'Table {table_name} truncated successfully.'))


if __name__ == "__main__":
    batch_script()